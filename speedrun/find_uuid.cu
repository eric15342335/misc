#include <cuda_runtime.h>

#include <cinttypes>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

namespace {

constexpr int kThreadsPerBlock = 256;
constexpr int kResidentWaves = 2;
constexpr unsigned int kPollInterval = 256U;
constexpr unsigned int kPollMask = kPollInterval - 1U;
constexpr unsigned int kRequiredZeroBits = 34;
constexpr std::uint64_t kMaxCounter = UINT64_C(1) << 58;
constexpr std::uint64_t kDefaultBatchSize = UINT64_C(1) << 25;


static constexpr std::uint64_t kHostK[80] = {
    UINT64_C(0x428a2f98d728ae22), UINT64_C(0x7137449123ef65cd), UINT64_C(0xb5c0fbcfec4d3b2f), UINT64_C(0xe9b5dba58189dbbc),
    UINT64_C(0x3956c25bf348b538), UINT64_C(0x59f111f1b605d019), UINT64_C(0x923f82a4af194f9b), UINT64_C(0xab1c5ed5da6d8118),
    UINT64_C(0xd807aa98a3030242), UINT64_C(0x12835b0145706fbe), UINT64_C(0x243185be4ee4b28c), UINT64_C(0x550c7dc3d5ffb4e2),
    UINT64_C(0x72be5d74f27b896f), UINT64_C(0x80deb1fe3b1696b1), UINT64_C(0x9bdc06a725c71235), UINT64_C(0xc19bf174cf692694),
    UINT64_C(0xe49b69c19ef14ad2), UINT64_C(0xefbe4786384f25e3), UINT64_C(0x0fc19dc68b8cd5b5), UINT64_C(0x240ca1cc77ac9c65),
    UINT64_C(0x2de92c6f592b0275), UINT64_C(0x4a7484aa6ea6e483), UINT64_C(0x5cb0a9dcbd41fbd4), UINT64_C(0x76f988da831153b5),
    UINT64_C(0x983e5152ee66dfab), UINT64_C(0xa831c66d2db43210), UINT64_C(0xb00327c898fb213f), UINT64_C(0xbf597fc7beef0ee4),
    UINT64_C(0xc6e00bf33da88fc2), UINT64_C(0xd5a79147930aa725), UINT64_C(0x06ca6351e003826f), UINT64_C(0x142929670a0e6e70),
    UINT64_C(0x27b70a8546d22ffc), UINT64_C(0x2e1b21385c26c926), UINT64_C(0x4d2c6dfc5ac42aed), UINT64_C(0x53380d139d95b3df),
    UINT64_C(0x650a73548baf63de), UINT64_C(0x766a0abb3c77b2a8), UINT64_C(0x81c2c92e47edaee6), UINT64_C(0x92722c851482353b),
    UINT64_C(0xa2bfe8a14cf10364), UINT64_C(0xa81a664bbc423001), UINT64_C(0xc24b8b70d0f89791), UINT64_C(0xc76c51a30654be30),
    UINT64_C(0xd192e819d6ef5218), UINT64_C(0xd69906245565a910), UINT64_C(0xf40e35855771202a), UINT64_C(0x106aa07032bbd1b8),
    UINT64_C(0x19a4c116b8d2d0c8), UINT64_C(0x1e376c085141ab53), UINT64_C(0x2748774cdf8eeb99), UINT64_C(0x34b0bcb5e19b48a8),
    UINT64_C(0x391c0cb3c5c95a63), UINT64_C(0x4ed8aa4ae3418acb), UINT64_C(0x5b9cca4f7763e373), UINT64_C(0x682e6ff3d6b2b8a3),
    UINT64_C(0x748f82ee5defb2fc), UINT64_C(0x78a5636f43172f60), UINT64_C(0x84c87814a1f0ab72), UINT64_C(0x8cc702081a6439ec),
    UINT64_C(0x90befffa23631e28), UINT64_C(0xa4506cebde82bde9), UINT64_C(0xbef9a3f7b2c67915), UINT64_C(0xc67178f2e372532b),
    UINT64_C(0xca273eceea26619c), UINT64_C(0xd186b8c721c0c207), UINT64_C(0xeada7dd6cde0eb1e), UINT64_C(0xf57d4f7fee6ed178),
    UINT64_C(0x06f067aa72176fba), UINT64_C(0x0a637dc5a2c898a6), UINT64_C(0x113f9804bef90dae), UINT64_C(0x1b710b35131c471b),
    UINT64_C(0x28db77f523047d84), UINT64_C(0x32caab7b40c72493), UINT64_C(0x3c9ebe0a15c9bebc), UINT64_C(0x431d67c49c100d4c),
    UINT64_C(0x4cc5d4becb3e42b6), UINT64_C(0x597f299cfc657e2a), UINT64_C(0x5fcb6fab3ad6faec), UINT64_C(0x6c44198c4a475817),
};

__constant__ std::uint64_t kDeviceK[80];

struct alignas(16) DeviceResult {
        unsigned int found;
        unsigned int padding;
        unsigned long long counter;
};

#define CUDA_CHECK(call)                                                                                                   \
    do {                                                                                                                   \
        const cudaError_t cuda_status_ = (call);                                                                           \
        if (cuda_status_ != cudaSuccess) {                                                                                 \
            std::fprintf(stderr, "%s:%d: CUDA error: %s\n", __FILE__, __LINE__, cudaGetErrorString(cuda_status_));         \
            std::exit(EXIT_FAILURE);                                                                                       \
        }                                                                                                                  \
    } while (false)

__host__ __device__ __forceinline__ std::uint64_t rotr64(std::uint64_t x, unsigned int n) {
    return (x >> n) | (x << (64U - n));
}

__host__ __device__ __forceinline__ std::uint64_t choose64(std::uint64_t x, std::uint64_t y, std::uint64_t z) {
    return (x & y) ^ (~x & z);
}

__host__ __device__ __forceinline__ std::uint64_t majority64(std::uint64_t x, std::uint64_t y, std::uint64_t z) {
    return (x & y) ^ (x & z) ^ (y & z);
}

__host__ __device__ __forceinline__ std::uint64_t big_sigma0(std::uint64_t x) {
    return rotr64(x, 28U) ^ rotr64(x, 34U) ^ rotr64(x, 39U);
}

__host__ __device__ __forceinline__ std::uint64_t big_sigma1(std::uint64_t x) {
    return rotr64(x, 14U) ^ rotr64(x, 18U) ^ rotr64(x, 41U);
}

__host__ __device__ __forceinline__ std::uint64_t small_sigma0(std::uint64_t x) {
    return rotr64(x, 1U) ^ rotr64(x, 8U) ^ (x >> 7U);
}

__host__ __device__ __forceinline__ std::uint64_t small_sigma1(std::uint64_t x) {
    return rotr64(x, 19U) ^ rotr64(x, 61U) ^ (x >> 6U);
}

__device__ __forceinline__ std::uint64_t candidate_h0(std::uint64_t prefix_word, std::uint64_t suffix_word,
                                                      std::uint64_t counter) {
    const std::uint32_t group2 = static_cast<std::uint32_t>(counter & 0xffffU);
    const std::uint32_t group3 = static_cast<std::uint32_t>((counter >> 16U) & 0x0fffU);
    const std::uint32_t variant = static_cast<std::uint32_t>((counter >> 28U) & 0x3U);
    const std::uint32_t group4 = static_cast<std::uint32_t>((counter >> 30U) & 0x0fffU);
    const std::uint32_t group5 = static_cast<std::uint32_t>((counter >> 42U) & 0xffffU);

    const std::uint64_t word0 =
        (prefix_word << 32U) | (static_cast<std::uint64_t>(group2) << 16U) | UINT64_C(0x4000) | group3;
    const std::uint64_t word1 = (static_cast<std::uint64_t>(UINT32_C(0x8000) | (variant << 12U) | group4) << 48U) |
                                (static_cast<std::uint64_t>(group5) << 32U) | suffix_word;

    // A 16-word rolling schedule prevents the 80-word schedule from spilling to
    // local memory. Full unrolling lets ptxas scalarize the ring into registers.
    std::uint64_t schedule[16] = {
        word0, word1, UINT64_C(0x8000000000000000), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128,
    };

    std::uint64_t a = UINT64_C(0x6a09e667f3bcc908);
    std::uint64_t b = UINT64_C(0xbb67ae8584caa73b);
    std::uint64_t c = UINT64_C(0x3c6ef372fe94f82b);
    std::uint64_t d = UINT64_C(0xa54ff53a5f1d36f1);
    std::uint64_t e = UINT64_C(0x510e527fade682d1);
    std::uint64_t f = UINT64_C(0x9b05688c2b3e6c1f);
    std::uint64_t g = UINT64_C(0x1f83d9abfb41bd6b);
    std::uint64_t h = UINT64_C(0x5be0cd19137e2179);

#pragma unroll 80
    for (int round = 0; round < 80; ++round) {
        std::uint64_t word;
        if (round < 16) {
            word = schedule[round];
        }
        else {
            word = small_sigma1(schedule[(round + 14) & 15]) + schedule[(round + 9) & 15] +
                   small_sigma0(schedule[(round + 1) & 15]) + schedule[round & 15];
            schedule[round & 15] = word;
        }

        const std::uint64_t temp1 = h + big_sigma1(e) + choose64(e, f, g) + kDeviceK[round] + word;
        const std::uint64_t temp2 = big_sigma0(a) + majority64(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    return a + UINT64_C(0x6a09e667f3bcc908);
}

__global__ __launch_bounds__(kThreadsPerBlock) void search_kernel(std::uint64_t prefix_word, std::uint64_t suffix_word,
                                                                  std::uint64_t batch_start, std::uint64_t batch_end,
                                                                  DeviceResult * result) {
    const std::uint64_t global_id = static_cast<std::uint64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    const std::uint64_t stride = static_cast<std::uint64_t>(gridDim.x) * blockDim.x;

    unsigned int poll_count = 0;
    for (std::uint64_t counter = batch_start + global_id; counter < batch_end; counter += stride) {
        if (((poll_count++ & kPollMask) == 0U) && atomicAdd(&result->found, 0U) != 0U) {
            return;
        }

        const std::uint64_t h0 = candidate_h0(prefix_word, suffix_word, counter);

        if ((h0 >> (64U - kRequiredZeroBits)) == 0U) {
            if (atomicCAS(&result->found, 0U, 1U) == 0U) {
                result->counter = static_cast<unsigned long long>(counter);
            }
            return;
        }
    }
}

std::uint64_t pack_hex8(const char text[8]) {
    std::uint64_t word = 0;
    for (int i = 0; i < 8; ++i) {
        const char value = text[i];
        const unsigned int nibble =
            (value <= '9') ? static_cast<unsigned int>(value - '0') : static_cast<unsigned int>(value - 'a' + 10);
        word = (word << 4U) | nibble;
    }
    return word;
}

constexpr char kHex[] = "0123456789abcdef";

void put_hex4(char * output, std::uint16_t value) {
    output[0] = kHex[(value >> 12U) & 15U];
    output[1] = kHex[(value >> 8U) & 15U];
    output[2] = kHex[(value >> 4U) & 15U];
    output[3] = kHex[value & 15U];
}

void put_hex3(char * output, std::uint16_t value) {
    output[0] = kHex[(value >> 8U) & 15U];
    output[1] = kHex[(value >> 4U) & 15U];
    output[2] = kHex[value & 15U];
}

void make_uuid(const char prefix[8], const char suffix[8], std::uint64_t counter, char uuid[37]) {
    std::memcpy(uuid, "00000000-0000-4000-8000-000000000000", 37);
    std::memcpy(uuid, prefix, 8);
    std::memcpy(uuid + 28, suffix, 8);

    const auto group2 = static_cast<std::uint16_t>(counter & 0xffffU);
    const auto group3 = static_cast<std::uint16_t>((counter >> 16U) & 0x0fffU);
    const unsigned int variant = static_cast<unsigned int>((counter >> 28U) & 3U);
    const auto group4 = static_cast<std::uint16_t>((counter >> 30U) & 0x0fffU);
    const auto group5 = static_cast<std::uint16_t>((counter >> 42U) & 0xffffU);

    put_hex4(uuid + 9, group2);
    put_hex3(uuid + 15, group3);
    uuid[19] = "89ab"[variant];
    put_hex3(uuid + 20, group4);
    put_hex4(uuid + 24, group5);
}

void sha512_uuid_host(const char uuid[36], unsigned char hash[64]) {
    unsigned char data[16];
    int data_index = 0;
    for (int uuid_index = 0; uuid_index < 36;) {
        if (uuid[uuid_index] == '-') {
            ++uuid_index;
            continue;
        }

        const char high = uuid[uuid_index];
        const char low = uuid[uuid_index + 1];
        const unsigned int high_nibble =
            (high <= '9') ? static_cast<unsigned int>(high - '0') : static_cast<unsigned int>(high - 'a' + 10);
        const unsigned int low_nibble =
            (low <= '9') ? static_cast<unsigned int>(low - '0') : static_cast<unsigned int>(low - 'a' + 10);
        data[data_index++] = static_cast<unsigned char>((high_nibble << 4U) | low_nibble);
        uuid_index += 2;
    }

    std::uint64_t schedule[80] = {};

    for (int i = 0; i < 2; ++i) {
        schedule[i] =
            (static_cast<std::uint64_t>(data[i * 8]) << 56U) | (static_cast<std::uint64_t>(data[i * 8 + 1]) << 48U) |
            (static_cast<std::uint64_t>(data[i * 8 + 2]) << 40U) | (static_cast<std::uint64_t>(data[i * 8 + 3]) << 32U) |
            (static_cast<std::uint64_t>(data[i * 8 + 4]) << 24U) | (static_cast<std::uint64_t>(data[i * 8 + 5]) << 16U) |
            (static_cast<std::uint64_t>(data[i * 8 + 6]) << 8U) | static_cast<std::uint64_t>(data[i * 8 + 7]);
    }

    schedule[2] = UINT64_C(0x8000000000000000);
    schedule[15] = 128;

    for (int i = 16; i < 80; ++i) {
        schedule[i] = small_sigma1(schedule[i - 2]) + schedule[i - 7] + small_sigma0(schedule[i - 15]) + schedule[i - 16];
    }

    std::uint64_t a = UINT64_C(0x6a09e667f3bcc908);
    std::uint64_t b = UINT64_C(0xbb67ae8584caa73b);
    std::uint64_t c = UINT64_C(0x3c6ef372fe94f82b);
    std::uint64_t d = UINT64_C(0xa54ff53a5f1d36f1);
    std::uint64_t e = UINT64_C(0x510e527fade682d1);
    std::uint64_t f = UINT64_C(0x9b05688c2b3e6c1f);
    std::uint64_t g = UINT64_C(0x1f83d9abfb41bd6b);
    std::uint64_t h = UINT64_C(0x5be0cd19137e2179);

    for (int i = 0; i < 80; ++i) {
        const std::uint64_t temp1 = h + big_sigma1(e) + choose64(e, f, g) + kHostK[i] + schedule[i];
        const std::uint64_t temp2 = big_sigma0(a) + majority64(a, b, c);
        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    const std::uint64_t state[8] = {
        a + UINT64_C(0x6a09e667f3bcc908), b + UINT64_C(0xbb67ae8584caa73b), c + UINT64_C(0x3c6ef372fe94f82b),
        d + UINT64_C(0xa54ff53a5f1d36f1), e + UINT64_C(0x510e527fade682d1), f + UINT64_C(0x9b05688c2b3e6c1f),
        g + UINT64_C(0x1f83d9abfb41bd6b), h + UINT64_C(0x5be0cd19137e2179),
    };

    for (int i = 0; i < 8; ++i) {
        hash[i * 8] = static_cast<unsigned char>(state[i] >> 56U);
        hash[i * 8 + 1] = static_cast<unsigned char>(state[i] >> 48U);
        hash[i * 8 + 2] = static_cast<unsigned char>(state[i] >> 40U);
        hash[i * 8 + 3] = static_cast<unsigned char>(state[i] >> 32U);
        hash[i * 8 + 4] = static_cast<unsigned char>(state[i] >> 24U);
        hash[i * 8 + 5] = static_cast<unsigned char>(state[i] >> 16U);
        hash[i * 8 + 6] = static_cast<unsigned char>(state[i] >> 8U);
        hash[i * 8 + 7] = static_cast<unsigned char>(state[i]);
    }
}

} // namespace

int main(int argc, char ** argv) {
    if (argc != 3) {
        std::fprintf(stderr, "usage: %s COMMIT_LAST8 FIXED_LAST8\n", argv[0]);
        return 2;
    }

    const char * inputs[2] = {argv[1], argv[2]};
    const char * names[2] = {"COMMIT_LAST8", "FIXED_LAST8"};
    char prefix[8];
    char suffix[8];
    char * normalized[2] = {prefix, suffix};

    for (int input = 0; input < 2; ++input) {
        if (std::strlen(inputs[input]) != 8) {
            std::fprintf(stderr, "%s must contain exactly 8 hex digits\n", names[input]);
            return 2;
        }
        for (int i = 0; i < 8; ++i) {
            const char value = inputs[input][i];
            const bool is_hex =
                (value >= '0' && value <= '9') || (value >= 'a' && value <= 'f') || (value >= 'A' && value <= 'F');
            if (!is_hex) {
                std::fprintf(stderr, "%s must contain only hexadecimal digits\n", names[input]);
                return 2;
            }
            normalized[input][i] = (value >= 'A' && value <= 'F') ? static_cast<char>(value - 'A' + 'a') : value;
        }
    }

    int device = 0;
    CUDA_CHECK(cudaGetDevice(&device));

    cudaDeviceProp properties{};
    CUDA_CHECK(cudaGetDeviceProperties(&properties, device));

    CUDA_CHECK(cudaMemcpyToSymbol(kDeviceK, kHostK, sizeof(kHostK)));

    DeviceResult initial_result{};
    DeviceResult * device_result = nullptr;
    CUDA_CHECK(cudaMalloc(&device_result, sizeof(DeviceResult)));
    CUDA_CHECK(cudaMemcpy(device_result, &initial_result, sizeof(DeviceResult), cudaMemcpyHostToDevice));

    int active_blocks_per_sm = 0;
    CUDA_CHECK(cudaOccupancyMaxActiveBlocksPerMultiprocessor(&active_blocks_per_sm, search_kernel, kThreadsPerBlock, 0));
    if (active_blocks_per_sm < 1) {
        active_blocks_per_sm = 1;
    }

    const int grid_blocks = properties.multiProcessorCount * active_blocks_per_sm * kResidentWaves;
    const std::uint64_t prefix_word = pack_hex8(prefix);
    const std::uint64_t suffix_word = pack_hex8(suffix);

    DeviceResult host_result{};
    for (std::uint64_t batch_start = 0; batch_start < kMaxCounter && host_result.found == 0U;) {
        const std::uint64_t batch_remaining = kMaxCounter - batch_start;
        const std::uint64_t batch_length = (batch_remaining < kDefaultBatchSize) ? batch_remaining : kDefaultBatchSize;
        const std::uint64_t batch_end = batch_start + batch_length;

        search_kernel<<<grid_blocks, kThreadsPerBlock>>>(prefix_word, suffix_word, batch_start, batch_end, device_result);
        CUDA_CHECK(cudaGetLastError());
        CUDA_CHECK(cudaDeviceSynchronize());
        CUDA_CHECK(cudaMemcpy(&host_result, device_result, sizeof(DeviceResult), cudaMemcpyDeviceToHost));

        batch_start = batch_end;
    }

    CUDA_CHECK(cudaFree(device_result));

    if (host_result.found == 0U) {
        return 1;
    }

    const std::uint64_t counter = static_cast<std::uint64_t>(host_result.counter);
    char uuid[37];
    unsigned char digest[64];
    make_uuid(prefix, suffix, counter, uuid);
    sha512_uuid_host(uuid, digest);

    std::printf("FOUND %s\nSHA512 ", uuid);
    for (unsigned char byte : digest) {
        std::printf("%02x", static_cast<unsigned int>(byte));
    }
    std::printf("\nCOUNTER %" PRIu64 "\n", counter);
    std::fflush(stdout);
    return 0;
}

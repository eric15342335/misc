// Compile with: g++ stage2.cpp -O3 -flto -march=native -s -Wall -Wextra
#include <windows.h>
#include <winuser.h> // Keep this include
#include <iostream>
#include <vector>
#include <chrono>
#include <thread> // For std::thread
#include <cmath>
#include <algorithm>
#include <string_view>
#include <string>
#include <sstream> // For formatting HUD string easily
#include <cstdio>  // For swprintf_s

// --- Define VK codes manually for compatibility ---
#ifndef VK_ESCAPE
#define VK_ESCAPE 0x1B
#endif
#ifndef VK_LEFT
#define VK_LEFT 0x25
#endif
#ifndef VK_RIGHT
#define VK_RIGHT 0x27
#endif
#ifndef VK_W // Use hex codes for letters
#define VK_W 0x57
#endif
#ifndef VK_A
#define VK_A 0x41
#endif
#ifndef VK_S
#define VK_S 0x53
#endif
#ifndef VK_D
#define VK_D 0x44
#endif
// --- End of VK code definitions ---


// MAP PARAMS
constexpr int mapWidth = 16;
constexpr int mapHeight = 16;
constexpr std::string_view map =
    "################"
    "#..............#"
    "#.......########"
    "#..............#"
    "#......##......#"
    "#......##......#"
    "#..............#"
    "###............#"
    "##.............#"
    "#......####..###"
    "#......#.......#"
    "#......#.......#"
    "#..............#"
    "#......#########"
    "#..............#"
    "################";

// --- Screen dimensions are now variable ---
int screenWidth = 120;    // Default console width (columns)
int screenHeight = 40;    // Default console height (rows)
// ---

constexpr float FOV = 3.14159f / 4.0f;   // 45 degrees
constexpr float FOV_div_2 = FOV / 2.0f; // Pre-calculated
constexpr float maxDepth = 16.0f;        // max rendering distance

// Define PI if needed
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// Function to get console size
bool GetConsoleSize(HANDLE hConsole, int& width, int& height) {
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    if (GetConsoleScreenBufferInfo(hConsole, &csbi)) {
        width = csbi.dwSize.X;
        // Height should be the window height, not buffer height, for visibility
        height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1;
        return true;
    }
    return false;
}

// Helper struct for boundary detection
struct CornerInfo {
    float dist;
    float dot;
};

// Pre-calculated cosine of the boundary angle check
constexpr float boundary_angle_check_val = 0.01f;
constexpr float cos_boundary_angle_check = 0.99995f; // cos(0.01f) approx

int main() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwBytesWritten = 0;

    // --- Initial Debug Info & Pause ---
    system("cls"); // Clear screen first
    std::cout << "Starting Raycaster Engine..." << std::endl;
    std::cout << "-----------------------------" << std::endl;
    std::cout << "Build: " << __DATE__ << " " << __TIME__ << std::endl;
    unsigned int core_count = std::thread::hardware_concurrency();
    if (core_count == 0) core_count = 1; // Avoid printing 0 cores
    std::cout << "Detected CPU Cores: " << core_count << std::endl;
    std::cout << "FOV: " << (FOV * 180.0f / M_PI) << " degrees" << std::endl;
    std::cout << "Max Render Depth: " << maxDepth << std::endl;
    std::cout << "-----------------------------" << std::endl;
    std::cout << "Initializing display..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2)); // Halt for 2 seconds
    system("cls"); // Clear screen again before game starts
    // --- End Initial Debug Info & Pause ---

    // --- Initial Console Size Detection ---
    if (!GetConsoleSize(hConsole, screenWidth, screenHeight)) {
        std::cerr << "Warning: Could not get console size. Using default "
                  << screenWidth << "x" << screenHeight << std::endl;
        // Optionally wait for user input here if it's critical
    }
    // ---

    // Initialize screen buffer with detected/default size
    std::wstring screen(screenWidth * screenHeight, L' ');
    SetConsoleActiveScreenBuffer(hConsole); // Ensure we're writing to the right buffer

    float halfScreenHeight_float = static_cast<float>(screenHeight) / 2.0f; // Pre-calculate

    float posX = 8.0f, posY = 8.0f; // player start
    float angle = 0.0f; // player angle
    constexpr float moveSpeed = 5.0f; // movement units/sec
    constexpr float rotSpeed = 1.5f;  // rotation radians/sec

    using clock = std::chrono::high_resolution_clock;
    auto tp1 = clock::now();
    std::chrono::duration<float> frameDuration(0); // To store frame processing time

    while (true) {
        // --- Check for Console Resize ---
        int newWidth, newHeight;
        if (GetConsoleSize(hConsole, newWidth, newHeight)) {
            if (newWidth != screenWidth || newHeight != screenHeight) {
                screenWidth = newWidth;
                screenHeight = newHeight;
                // Resize the screen buffer, fill with spaces
                screen.assign(screenWidth * screenHeight, L' ');
                // Optional: Clear console here if resizing causes artifacts
                // system("cls"); // This flickers, better to just overwrite
                halfScreenHeight_float = static_cast<float>(screenHeight) / 2.0f; // Update pre-calculated value
            }
        }
        // --- End Resize Check ---

        // Timing
        auto tp2 = clock::now();
        const auto elapsedTimeDuration = tp2 - tp1;
        tp1 = tp2;
        const float deltaTime = std::chrono::duration_cast<std::chrono::duration<float>>(elapsedTimeDuration).count();

        // Controls using GetAsyncKeyState
        if (GetAsyncKeyState(VK_ESCAPE) & 0x8000) break;
        if (GetAsyncKeyState(VK_LEFT) & 0x8000) angle -= rotSpeed * deltaTime;
        if (GetAsyncKeyState(VK_RIGHT) & 0x8000) angle += rotSpeed * deltaTime;

        float forwardInput = 0.0f;
        float strafeInput = 0.0f;
        if (GetAsyncKeyState(VK_W) & 0x8000) forwardInput += 1.0f;
        if (GetAsyncKeyState(VK_S) & 0x8000) forwardInput -= 1.0f;
        if (GetAsyncKeyState(VK_A) & 0x8000) strafeInput -= 1.0f;
        if (GetAsyncKeyState(VK_D) & 0x8000) strafeInput += 1.0f;

        float forwardDx = sinf(angle);
        float forwardDy = cosf(angle);
        float strafeDx = cosf(angle);
        float strafeDy = -sinf(angle);
        float moveDx = (forwardDx * forwardInput + strafeDx * strafeInput);
        float moveDy = (forwardDy * forwardInput + strafeDy * strafeInput);
        float moveMag = sqrtf(moveDx * moveDx + moveDy * moveDy);
        if (moveMag > 0.001f) {
            moveDx /= moveMag;
            moveDy /= moveMag;
        }
        float finalDx = moveDx * moveSpeed * deltaTime;
        float finalDy = moveDy * moveSpeed * deltaTime;
        float targetX = posX + finalDx;
        float targetY = posY + finalDy;

        // Check bounds before accessing map array
        int mapCheckX = static_cast<int>(targetX);
        int mapCheckY = static_cast<int>(targetY);
        if (mapCheckX >= 0 && mapCheckX < mapWidth && mapCheckY >= 0 && mapCheckY < mapHeight &&
            map[mapCheckY * mapWidth + mapCheckX] != '#')
        {
            posX = targetX;
            posY = targetY;
        }

        // Render
        // Check if screen dimensions are valid before rendering
        if (screenWidth <= 0 || screenHeight <= 0) {
             std::this_thread::sleep_for(std::chrono::milliseconds(50)); // Avoid busy-waiting if console is invalid
             continue; // Skip rendering and output if dimensions are bad
        }

        // --- Manual Threading for Rendering --- 
        unsigned int num_threads = std::thread::hardware_concurrency();
        if (num_threads == 0) num_threads = 2; // Fallback if hardware_concurrency returns 0 or 1 (still use 2 for some parallelism)
        if (static_cast<unsigned int>(screenWidth) < num_threads) num_threads = std::max(1, screenWidth); // Don't use more threads than columns

        std::vector<std::thread> threads;
        threads.reserve(num_threads);

        int columns_per_thread_base = screenWidth / num_threads;
        int remaining_columns = screenWidth % num_threads;
        int current_start_x = 0;

        // Capture variables needed by threads. Capture by value for those that might change
        // or to ensure each thread has a consistent copy for its workload.
        // 'screen' is captured by reference as it's the output target.
        // 'map' is a constexpr string_view, safe to capture by reference or value.
        const float current_angle = angle;
        const float current_posX = posX;
        const float current_posY = posY;
        const int current_screenWidth = screenWidth;
        const int current_screenHeight = screenHeight;
        const float current_halfScreenHeight_float = halfScreenHeight_float;

        for (unsigned int i = 0; i < num_threads; ++i) {
            int columns_for_this_thread = columns_per_thread_base + (i < static_cast<unsigned int>(remaining_columns) ? 1 : 0);
            if (columns_for_this_thread == 0) continue;

            int thread_start_x = current_start_x;
            int thread_end_x = current_start_x + columns_for_this_thread;
            current_start_x = thread_end_x;

            threads.emplace_back([
                &screen, thread_start_x, thread_end_x,
                current_angle, current_screenWidth, current_screenHeight,
                current_posX, current_posY,
                current_halfScreenHeight_float
            ]() {
                for (int x = thread_start_x; x < thread_end_x; x++) {
                    const float rayAngle = (current_angle - FOV_div_2) + ((static_cast<float>(x) / static_cast<float>(current_screenWidth)) * FOV);
                    float distToWall = 0.0f;
                    bool hitWall = false;
                    bool boundary = false;
                    const float eyeX = sinf(rayAngle);
                    const float eyeY = cosf(rayAngle);

                    while (!hitWall && distToWall < maxDepth) {
                        distToWall += 0.05f;
                        const int testX = static_cast<int>(current_posX + eyeX * distToWall);
                        const int testY = static_cast<int>(current_posY + eyeY * distToWall);

                        if (testX < 0 || testX >= mapWidth || testY < 0 || testY >= mapHeight) {
                            hitWall = true;
                            distToWall = maxDepth;
                        } else if (map[testY * mapWidth + testX] == '#') {
                            hitWall = true;
                            CornerInfo corners[4];
                            int k = 0;
                            for (int tx = 0; tx < 2; tx++) {
                                for (int ty = 0; ty < 2; ty++) {
                                    const float vx = static_cast<float>(testX) + tx - current_posX;
                                    const float vy = static_cast<float>(testY) + ty - current_posY;
                                    const float d = sqrtf(vx*vx + vy*vy);
                                    float current_dot = (d > 0.001f) ? ((eyeX*vx/d) + (eyeY*vy/d)) : 1.0f;
                                    corners[k++] = {d, std::max(-1.0f, std::min(1.0f, current_dot))};
                                }
                            }
                            std::sort(corners, corners + 4, [](const CornerInfo& a, const CornerInfo& b) {
                                return a.dist < b.dist;
                            });
                            if (corners[0].dot > cos_boundary_angle_check) boundary = true;
                            if (!boundary && corners[1].dot > cos_boundary_angle_check) boundary = true;
                        }
                    }

                    distToWall = std::max(0.1f, distToWall); // Clamp minimum distance for perspective calc

                    const int ceiling = static_cast<int>(current_halfScreenHeight_float - static_cast<float>(current_screenHeight) / distToWall);
                    const int floor = current_screenHeight - ceiling;
                    wchar_t shade = L' ';
                    if (distToWall <= maxDepth/4.0f)       shade = 0x2588;
                    else if (distToWall < maxDepth/3.0f)   shade = 0x2593;
                    else if (distToWall < maxDepth/2.0f)   shade = 0x2592;
                    else if (distToWall < maxDepth)        shade = 0x2591;
                    else                                   shade = L' ';
                    if (boundary) shade = L' ';

                    for (int y = 0; y < current_screenHeight; y++) {
                        size_t screenIndex = static_cast<size_t>(y) * current_screenWidth + x;
                        if (screenIndex >= screen.length()) continue;
                        if (y < ceiling)
                            screen[screenIndex] = L' ';
                        else if (y > ceiling && y <= floor)
                            screen[screenIndex] = shade;
                        else {
                            const float b = 1.0f - ((static_cast<float>(y) - current_halfScreenHeight_float)/current_halfScreenHeight_float);
                            wchar_t floorShade = L' ';
                            if (b < 0.25)       floorShade = L'#';
                            else if (b < 0.5)   floorShade = L'x';
                            else if (b < 0.75)  floorShade = L'.';
                            else if (b < 0.9)   floorShade = L'-';
                            else                floorShade = L' ';
                            screen[screenIndex] = floorShade;
                        }
                    }
                }
            });
        }

        for (auto& t : threads) {
            if (t.joinable()) {
                t.join();
            }
        }
        // --- End Manual Threading ---

        // HUD and Mini-map display
        // Clear only the necessary HUD area (first line)
        // Using std::fill_n for potentially cleaner/faster fill if screen is large enough
        if (!screen.empty() && screenWidth > 0) { // Ensure screen is not empty and screenWidth is positive
            std::fill_n(screen.begin(), std::min(static_cast<size_t>(screenWidth), screen.length()), L' ');
        }

        wchar_t hudBuffer[256]; // Buffer for swprintf_s
        float fps = (deltaTime > 0.0f) ? (1.0f / deltaTime) : 0.0f;
        float currentFrameTimeMs = std::chrono::duration_cast<std::chrono::duration<float, std::milli>>(frameDuration).count();

        int chars_written = swprintf_s(hudBuffer, sizeof(hudBuffer)/sizeof(hudBuffer[0]),
            L"X:%.2f Y:%.2f A:%.2f | Map(%d,%d) | FPS:%.0f | dT:%.2fms | FrameT:%.2fms | Size:%dx%d",
            posX, posY, angle,
            static_cast<int>(posX), static_cast<int>(posY),
            fps,
            deltaTime * 1000.0f,
            currentFrameTimeMs,
            screenWidth, screenHeight);

        std::wstring hudStr;
        if (chars_written > 0) {
            hudStr.assign(hudBuffer, chars_written);
        } else {
            hudStr = L"HUD Error"; // Fallback
        }
        
        size_t hudLen = std::min(static_cast<size_t>(screenWidth), hudStr.length());
        // Use std::copy or manual loop for safety if hudStr is longer than screenWidth
        // The existing loop is safe. For potentially more idiomatic C++, std::copy:
        if (hudLen > 0 && hudLen <= screen.length()) { // Ensure hudLen is valid for screen
             std::copy_n(hudStr.c_str(), hudLen, screen.begin());
        } else if (hudLen > 0) { // If hudLen is too large for screen (should not happen with screenWidth limit)
            // Fallback to manual copy with checks, or ensure screen is always large enough
            for(size_t i = 0; i < hudLen && i < screen.length(); ++i) {
                 screen[i] = hudStr[i];
            }
        }

        // Display mini map (check bounds)
        int miniMapStartY = 2; // Start minimap below HUD
        for (int nx = 0; nx < mapWidth; nx++) {
            for (int ny = 0; ny < mapHeight; ny++) {
                int screenY = ny + miniMapStartY;
                if (nx < screenWidth && screenY < screenHeight) { // Check bounds before drawing
                     size_t screenIndex = static_cast<size_t>(screenY) * screenWidth + nx;
                     if (screenIndex < screen.length()) { // Double check index
                         screen[screenIndex] = map[ny * mapWidth + nx];
                     }
                }
            }
        }
        int playerMiniMapX = static_cast<int>(posX);
        int playerMiniMapY = static_cast<int>(posY);
        playerMiniMapX = std::max(0, std::min(mapWidth - 1, playerMiniMapX));
        playerMiniMapY = std::max(0, std::min(mapHeight - 1, playerMiniMapY));
        int playerScreenY = playerMiniMapY + miniMapStartY;
        if (playerMiniMapX < screenWidth && playerScreenY < screenHeight) { // Check bounds
             size_t screenIndex = static_cast<size_t>(playerScreenY) * screenWidth + playerMiniMapX;
             if (screenIndex < screen.length()) {
                 screen[screenIndex] = L'P';
             }
        }

        // Output to console
        COORD coord = {0, 0};
        SetConsoleCursorPosition(hConsole, coord); // Reset cursor position
        WriteConsoleOutputCharacterW(hConsole, screen.c_str(), screenWidth * screenHeight, coord, &dwBytesWritten);

        // Calculate frame duration for HUD (Frame Limiter removed)
        auto frameEndTime = clock::now();
        frameDuration = frameEndTime - tp2;
    }

    // Optional: Clear screen or restore console state on exit
    system("cls"); // Example: Clear screen on exit

    return 0;
}

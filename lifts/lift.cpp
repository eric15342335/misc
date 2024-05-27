/*
g++ lift.cpp -Wall -Wextra -pedantic -Wunused -Wshadow -O3 -flto -o lift
./lift
*/

#include <algorithm>
#include <cassert>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

enum {
    liftCapacity = 20,
    maxRound = 12,
    minRound = 5,
    minRoundDifference = 4,
    minNumPeople = 0,
    maxNumPeople = liftCapacity * maxRound,
    minDefaultNumPeople = liftCapacity * minRound,
    normDistSDBound = 2,
    coutWidth = 8
};

#define numQueues 2
#define numLifts numQueues
#if numQueues == 2
enum {
    lift1MeanWaitingTime = 10,
    lift1StdDevWaitingTime = 2,
    lift2MeanWaitingTime = 12,
    lift2StdDevWaitingTime = 4,
    isLift1FasterThanLift2 = true
};
#else
#error "FeatureNotImplemented: Number of queues must be equal to 2"
#endif

class Lift {
    public:
        const unsigned int id;
        const unsigned int meanWaitingTime;
        const unsigned int stdDevWaitingTime;
        const unsigned int capacity = liftCapacity;

        Lift(unsigned int _id, unsigned int _meanWaitingTime, unsigned int _stdDevWaitingTime)
            : id(_id), meanWaitingTime(_meanWaitingTime), stdDevWaitingTime(_stdDevWaitingTime) {};

        // Print the information of the lift via <<
        friend auto operator<<(std::ostream & os, const Lift & lift) -> std::ostream & {
            os << lift.id << " " << lift.meanWaitingTime << " " << lift.stdDevWaitingTime;
            return os;
        }

        // Generate a random waiting time based on the mean and standard deviation
        // using a truncated normal distribution to avoid negative waiting time
        [[nodiscard]] auto generateWaitingTime() const -> unsigned int {
            assert(meanWaitingTime - stdDevWaitingTime * normDistSDBound > 0);

            unsigned int const seed = std::chrono::system_clock::now().time_since_epoch().count();
            std::default_random_engine generator(seed);
            std::normal_distribution<double> distribution(meanWaitingTime, stdDevWaitingTime);
            double waitingTime = distribution(generator);

            if (waitingTime < meanWaitingTime - stdDevWaitingTime * normDistSDBound) {
                waitingTime = meanWaitingTime - stdDevWaitingTime * normDistSDBound;
            }
            else if (waitingTime > meanWaitingTime + stdDevWaitingTime * normDistSDBound) {
                waitingTime = meanWaitingTime + stdDevWaitingTime * normDistSDBound;
            }
            return static_cast<unsigned int>(waitingTime);
        }

        // Get the time when the lift will be available
        [[nodiscard]] auto getAvailableTime(unsigned int currentTime) const -> unsigned int {
            return currentTime + generateWaitingTime();
        }
};

class Queue {
    public:
        unsigned int id;
        unsigned int numPeople;

        // Which lift is the queue for
        const Lift * lift;

        Queue(unsigned int _id, unsigned int _numPeople, Lift * _lift)
            : id(_id), numPeople(_numPeople), lift(_lift) {
            static_assert(
                numQueues == numLifts, "Number of queues must be equal to number of lifts");
            static_assert(
                numQueues > minNumPeople, "Number of queues must be greater than minNumPeople");
            assert(_lift != nullptr);
        }

        // Print the information of the queue via <<
        friend auto operator<<(std::ostream & os, const Queue & queue) -> std::ostream & {
            os << queue.id << " " << queue.numPeople << " " << *queue.lift;
            return os;
        }

        // Store waiting time for each queue
        unsigned int waitingTime = 0;

        // Compare the waiting time of two queues
        auto operator<(const Queue & queue) const -> bool {
            return this->waitingTime < queue.waitingTime;
        }
};

auto simulateTwoQueues(std::vector<Queue *> queues) -> decltype(Queue::id) {
    // Simulate the total time taken for the lift to serve all the queues
    for (Queue * queue : queues) {
        while (queue->numPeople > minNumPeople) {
            queue->waitingTime = queue->lift->getAvailableTime(queue->waitingTime);
            if (queue->numPeople > queue->lift->capacity) {
                queue->numPeople -= queue->lift->capacity;
            }
            else {
                queue->numPeople = minNumPeople;
            }
        }
    }
    // Return the fastest queue id
    return (*std::min_element(queues.begin(), queues.end()))->id;
}

auto main() -> int {
    // Result vector
    std::vector<std::string> const headers = {"Queue1", "Queue2", "Lift1", "Lift2", "Fastest"};
    struct results {
        public:
            unsigned int queueLength;
            unsigned int queue2Length;
            unsigned int lift1WaitingTime;
            unsigned int lift2WaitingTime;
            unsigned int fastestQueueId;
    } __attribute__((aligned(32)));
    std::vector<results> rows;
    // Simulate which queue is the fastest under every possible scenario
    // which is achieved by generating random queue length and lift waiting time
    static_assert(isLift1FasterThanLift2 != 0u, "Lift 1 must be faster than Lift 2");
    for (unsigned int queueLength = minDefaultNumPeople; queueLength <= maxNumPeople;
         queueLength += liftCapacity) {
        for (unsigned int queue2Length = minDefaultNumPeople;
             queue2Length <= queueLength - minRoundDifference; queue2Length += liftCapacity) {
            std::vector<Queue *> queues;

            // todo: add more queues
            queues.push_back(new Queue(numQueues - 1, queueLength,
                new Lift(0, lift1MeanWaitingTime, lift1StdDevWaitingTime)));
            queues.push_back(new Queue(numQueues, queue2Length,
                new Lift(1, lift2MeanWaitingTime, lift2StdDevWaitingTime)));

            auto fastestQueueId = simulateTwoQueues(queues);

            // Add the result only if the fastest queue is different from the previous
            // simulation Otherwise, remove the last simulation and add the new one
            if (!rows.empty() && rows.back().fastestQueueId == fastestQueueId &&
                rows.back().queueLength == queueLength) {
                rows.pop_back();
            }
            results const result = {queueLength, queue2Length, (*queues.begin())->waitingTime,
                (*++queues.begin())->waitingTime, fastestQueueId};
            rows.push_back(result);

            // Free the memory
            for (Queue * queue : queues) {
                delete queue->lift;
                delete queue;
            }
        }
    }

    // Print the results
    for (const std::string & header : headers) {
        std::cout << std::setw(coutWidth) << header;
    }
    std::cout << '\n';
    for (const results & row : rows) {
        std::cout << std::setw(coutWidth) << row.queueLength;
        std::cout << std::setw(coutWidth) << row.queue2Length;
        std::cout << std::setw(coutWidth) << row.lift1WaitingTime;
        std::cout << std::setw(coutWidth) << row.lift2WaitingTime;
        std::cout << std::setw(coutWidth) << row.fastestQueueId;
        std::cout << '\n';
    }
    return 0;
}

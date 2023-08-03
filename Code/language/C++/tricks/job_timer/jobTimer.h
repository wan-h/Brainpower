#ifndef JOB_TIMER_H
#define JOB_TIMER_H

#include <atomic>
#include <boost/asio.hpp>
#include <boost/scoped_ptr.hpp>
#include <boost/thread.hpp>

class JobTimerListener {
public:
    virtual void onTimeout() = 0;
};

class JobTimer {
public:
    JobTimer(unsigned int frequency, JobTimerListener* listener);
    ~JobTimer();

    void start();
    void stop();

private:
    void onTimeout(const boost::system::error_code& ec);
    void handleJob();

private:
    std::atomic<bool> m_isClosing;
    bool m_isRunning;

    unsigned int m_interval;
    JobTimerListener* m_listener;

    boost::scoped_ptr<boost::asio::deadline_timer> m_timer;
};

#endif
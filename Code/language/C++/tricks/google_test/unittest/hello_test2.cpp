#include <iostream>
#include <gtest/gtest.h>

class FooTest: public testing::Test
{
protected:
    // 每一个测试开始前的set-up
    FooTest()
    {
        std::cout << "Test set-up" << std::endl;
    }
    // 每一个测试结束后的clean-up
    ~FooTest() override
    {
        std::cout << "Test clean-up" << std::endl;
    }
    // 每一个测试开始前的set-up
    // 在构造函数之后立即执行
    void SetUp() override
    {
        std::cout << "Test SetUp" << std::endl;
    }
    // 每一个测试结束后的clean-up
    // 在析构函数之前立即执行
    void TearDown() override
    {
        std::cout << "Test TearDown" << std::endl;
    }
    // 该场景第一个测试开始前执行
    static void SetUpTestCase()
    {
        std::cout << "SetUpTestCase" << std::endl;
    }
    // 该场景最后一个测试结束后执行
    static void TearDownTestCase() {
        std::cout << "TearDownTestCase" << std::endl;
    }
};

TEST_F(FooTest, test1)
{
    EXPECT_EQ(0, 0);
}

TEST_F(FooTest, test2)
{
    EXPECT_EQ(1, 1);
}
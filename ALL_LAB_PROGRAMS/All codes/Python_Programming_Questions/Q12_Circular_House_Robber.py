# QUESTION 12: HOUSE ROBBER II - MAXIMUM MONEY IN A CIRCULAR STREET

def rob_linear(nums):
    prev2 = 0
    prev1 = 0

    for money in nums:
        current = max(prev1, prev2 + money)
        prev2 = prev1
        prev1 = current

    return prev1


def house_robber(nums):
    n = len(nums)

    if n == 0:
        return 0
    if n == 1:
        return nums[0]

    option1 = rob_linear(nums[:-1])
    option2 = rob_linear(nums[1:])
    return max(option1, option2)


nums = list(map(int, input("Enter money in each house: ").split()))
result = house_robber(nums)
print("Maximum money that can be robbed:", result)

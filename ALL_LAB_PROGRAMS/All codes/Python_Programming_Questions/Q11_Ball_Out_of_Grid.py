# QUESTION 11: COUNT WAYS TO MOVE A BALL OUT OF A GRID

def find_paths(m, n, N, i, j):
    MOD = 10**9 + 7
    dp = [[0] * n for _ in range(m)]
    dp[i][j] = 1
    total_paths = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for step in range(N):
        next_dp = [[0] * n for _ in range(m)]

        for r in range(m):
            for c in range(n):
                if dp[r][c] == 0:
                    continue

                for dr, dc in directions:
                    nr = r + dr
                    nc = c + dc

                    if nr < 0 or nr >= m or nc < 0 or nc >= n:
                        total_paths = (total_paths + dp[r][c]) % MOD
                    else:
                        next_dp[nr][nc] = (next_dp[nr][nc] + dp[r][c]) % MOD

        dp = next_dp

    return total_paths


m = int(input("Enter number of rows: "))
n = int(input("Enter number of columns: "))
N = int(input("Enter maximum number of steps: "))
i = int(input("Enter starting row: "))
j = int(input("Enter starting column: "))

result = find_paths(m, n, N, i, j)
print("Number of ways to move out:", result)

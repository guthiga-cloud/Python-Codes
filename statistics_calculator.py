# statistics_calculator.py
# Calculate statistical measures

import statistics

def main():
    data = [23, 45, 12, 67, 34, 89, 45, 23, 56, 78, 34, 45]
    
    print("=== STATISTICS CALCULATOR ===")
    print(f"Data Set: {data}")
    print(f"Number of elements: {len(data)}\n")
    
    # Mean
    mean = statistics.mean(data)
    print(f"1. Mean (Average): {mean:.2f}")
    
    # Median
    median = statistics.median(data)
    print(f"2. Median: {median}")
    
    # Mode
    try:
        mode = statistics.mode(data)
        print(f"3. Mode: {mode}")
    except statistics.StatisticsError:
        print("3. Mode: No unique mode found")
    
    # Range
    data_range = max(data) - min(data)
    print(f"4. Range: {data_range}")
    
    # Variance
    variance = statistics.variance(data)
    print(f"5. Variance: {variance:.2f}")
    
    # Standard Deviation
    std_deviation = statistics.stdev(data)
    print(f"6. Standard Deviation: {std_deviation:.2f}")

if __name__ == "__main__":
    main()

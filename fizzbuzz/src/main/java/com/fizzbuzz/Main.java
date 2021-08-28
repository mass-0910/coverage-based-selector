package com.fizzbuzz;

public class Main {
    public static void main(String[] args) {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz(0);
        bugFizzBuzz0.allBuggyFizzBuzz();
        // Undeclared exception!
        bugFizzBuzz0.allBuggyFizzBuzz();
        bugFizzBuzz0.output();
    }
}
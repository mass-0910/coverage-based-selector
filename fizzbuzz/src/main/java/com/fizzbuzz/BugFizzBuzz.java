package com.fizzbuzz;

import java.util.ArrayList;

public class BugFizzBuzz {

    private int start;
    private int[] int_array;
    private final int array_size = 10;
    private String[] string_array = new String[array_size];

    public BugFizzBuzz( int start ) {
        this.start = start;
        makeIntArray();
    }

    public void allCorrectFizzBuzz() {
        for( int i = 0; i < array_size; i++ ) {
            string_array[i] = correctFizzBuzz(int_array[i]);
        }
    }

    public void allBuggyFizzBuzz() {
        for( int i = 0; i < array_size; i++ ) {
            string_array[i] = buggyFizzBuzz(int_array[i]);
        }
    }

    public void output() {
        System.out.print("[");
        for( String str : string_array ) {
            System.out.print(str);
        }
        System.out.println("]");
    }

    private void makeIntArray() {
        int_array = new int[array_size];
        for( int i = start; i < start+array_size; i++ ) {
            int_array[i-start] = i;
        }
    }

    private String correctFizzBuzz( int num ) {
        if ( num % 3 == 0 && num % 5 == 0 ) {
            return "FizzBuzz";
        }else if ( num % 3 == 0 ) {
            return "Fizz";
        }else if ( num % 5 == 0 ) {
            return "Buzz";
        }
        return String.valueOf(num);
    }

    private String buggyFizzBuzz( int num ) {
        if ( num % 3 == 0 ) {
            return "Fizz";
        }else if ( num % 5 == 0 ) {
            return "Buzz";
        }else if ( num % 3 == 0 && num % 5 == 0 ) {
            return "FizzBuzz";
        }
        return String.valueOf(num);
    }
}

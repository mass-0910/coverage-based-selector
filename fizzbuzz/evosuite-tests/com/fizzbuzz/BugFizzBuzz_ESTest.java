/*
 * This file was automatically generated by EvoSuite
 * Fri Feb 05 01:41:33 GMT 2021
 */

package com.fizzbuzz;

import org.junit.Test;
import static org.junit.Assert.*;
import com.fizzbuzz.BugFizzBuzz;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = false, useVFS = false, useVNET = false, resetStaticState = true, separateClassLoader = false)
public class BugFizzBuzz_ESTest extends BugFizzBuzz_ESTest_scaffolding {

    @Test(timeout = 4000)
    public void test0()  throws Throwable  {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz((-1855));
        bugFizzBuzz0.allBuggyFizzBuzz();
    }

    @Test(timeout = 4000)
    public void test1()  throws Throwable  {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz((-16));
        bugFizzBuzz0.allCorrectFizzBuzz();
    }

    @Test(timeout = 4000)
    public void test2()  throws Throwable  {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz(1754);
        bugFizzBuzz0.allBuggyFizzBuzz();
    }

    @Test(timeout = 4000)
    public void test3()  throws Throwable  {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz(1754);
        bugFizzBuzz0.output();
    }

    @Test(timeout = 4000)
    public void test4()  throws Throwable  {
        BugFizzBuzz bugFizzBuzz0 = new BugFizzBuzz(1754);
        bugFizzBuzz0.allCorrectFizzBuzz();
    }
}

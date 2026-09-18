/*
 * rtest.cpp
 *
 * Test random.hpp
 * Draw random points in unit cube. Allows search for correlations.
 * All I generate is the points to render in Python.
 *
 * BCollett 9/26
 */
#include <iostream>
#include <fstream>

#include "random.hpp"

int main(int argn, char *argv[]) {
	CRand64 gen(0x0BCFACE0);
	int npoint = 100;
	std::fstream fs;
	fs.open ("rtest.txt", std::fstream::out | std::fstream::app);
	
	fs << "npoint " << npoint << std::endl;
	
	for (int i = 0; i < npoint; i++) {
		double x = gen.rand();
		double y = gen.rand();
		double x = gen.rand();
		fs << x << ", " y << ", " z << std::endl;
	}
	
	fs.close();
	return npoint;
}
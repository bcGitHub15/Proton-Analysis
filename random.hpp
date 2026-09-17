/*
 * Random.hpp
 *
 * A header-only version of my Random class.
 *
 * BCollett 9/26 based on much older work which in turn is based on a DrDobbs article.
 */
#ifndef _Random_hpp
#define _Random_hpp

#include <stdlib.h>

#include <math.h>
#include "Random.h"

class CRandom {
public:
	//
	//	Constructor takes seed.
	//
	CRandom(int seed = -1) { srand(seed); };
	virtual ~CRandom() {};
	//
	//	All it has are accessors that return randoms over
	//	various domains.
	//
	// Returns int on 0->Rand_Max as a double
	virtual double Rand() { return 1.0 * rand(); };				
	// largest random integer
	virtual double RandMax() { return 1.0 * RAND_MAX; };
	// double in domain rMin->rMax			
	virtual double Rand(double rMin, double rMax) { 
		return rMin + (rMax - rMin) * (Rand() / RandMax());
	}; 
	// double on 0->rmax
	virtual double Rand(double rMax) { return rMax * (Rand() / RandMax()); };	
//	virtual int Rand(int rMax);			// Returns int on 0->rMax
};

/*
 *	Rand64 is an implementation of the CRandom class that uses a
 *	a fully 64-bit combination generator taken from Mark Overton's
 *	Dr. Dobb's article
 *	http://www.drdobbs.com/tools/fast-high-quality-parallel-random-number/229625477
 *
 *	Originally BCollett 7/31/13
 */
#define rotl(r,n) (((r)<<(n)) | ((r)>>((8*sizeof(r))-(n))))

class CRand64 : public CRandom {
protected:
	//
	//	Instance vars are the stores for the three sub-cycle generators from which
	//	this is built. These three use different prime-period sub-cycles with the
	//	forms RERS, RES, and RESDRA.
	//
	uint64_t mGen1;
	uint64_t mGen2;
	uint64_t mGen3;
	uint64_t mCallCount;
	uint32_t mId;
public:	
	//
	//	Constructor takes seed.
	//
	CRand64(int seed = -1) {
		uint32_t n;
		mId = gGenNum++;
		mCallCount = 0;
		mGen1 =    914489ULL;
		mGen2 =   8675416ULL;
		mGen3 = 439754684ULL;
		for (n=((seed>>22)&0x3ff)+20; n>0; n--) { mGen1 = rotl(mGen1,8) - rotl(mGen1,29); }
		for (n=((seed>>11)&0x7ff)+20; n>0; n--) { mGen2 = rotl(mGen2,21) - mGen2;  mGen2 = rotl(mGen2,20); }
		for (n=((seed    )&0x7ff)+20; n>0; n--) { mGen3 = rotl(mGen3,42) - mGen3;  mGen3 = rotl(mGen3,14) + mGen3; }
	};;
	virtual ~CRand64() {};
	//
	//	Override two key accessors
	//
	// Rand() returns int on 0->Rand_Max
	// Combined period = 2^116.23
	// RERS period = 4758085248529 (prime)
	//
	virtual double Rand() {
		mGen1 = rotl(mGen1, 8) - rotl(mGen1, 29);													// RERS,	 period = 4758085248529 (prime)
		mGen2 = rotl(mGen2,21) - mGen2;  mGen2 = rotl(mGen2,20);	// RESR,   period = 3841428396121 (prime)
		mGen3 = rotl(mGen3,42) - mGen3;  mGen3 = mGen3 + rotl(mGen3,14);	// RESDRA, period = 5345004409 (prime)
		uint64_t rnd = mGen1 ^ mGen2 ^ mGen3;
		double num = rnd;
		double denom = (double) (0xFFFFFFFFFFFFFFFFLL);
		return (double) (num /denom);
	}			
	// largest random integer, which for this algorithm is 1.0
	virtual double RandMax() { return 1.0; };
};

#endif

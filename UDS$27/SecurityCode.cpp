#include <stdlib.h>
#include <stdio.h>

typedef unsigned char uint8;
typedef unsigned long uint32;
typedef unsigned long long uint64;

uint8 SecurityAccess_ComputeKey( uint8* inputSeed, uint8* KeyConstant,uint8* computedKey )
{
  uint8   result;
  uint8 *keyOutput;
  uint8 *Seed;
  uint8 idx, i;
  uint8 mask, x;
  uint8 secC[3], secF[8];

  uint8 kSecB2[2] = { 0x00u , 0x80u };
  uint8 kSecC2[2] = { 0x00u , 0x10u };
  uint8 kSecC1[2] = { 0x00u , 0x90u };
  uint8 kSecC0[2] = { 0x00u , 0x28u };

  result = 0U;

  /* Dereference output key for easier access */
  keyOutput = computedKey;

  /* Dereference seed for easier access */
  Seed = inputSeed;

  /* Initialize local variables */
  result = 0U;
  mask = 0x01u;
  x    = 0u;

  secF[0] = Seed[0];
  secF[1] = Seed[1];
  secF[2] = Seed[2];
  secF[3] = KeyConstant[0];
  secF[4] = KeyConstant[1];
  secF[5] = KeyConstant[2];
  secF[6] = KeyConstant[3];
  secF[7] = KeyConstant[4];

  secC[0] = 0xA9u;
  secC[1] = 0x41u;
  secC[2] = 0xC5u;

  for (i = 0u; i < 64u; i++)
  {
    idx = (uint8)(((mask & secF[x]) != 0u) ? (1u) : (0u));

    idx ^= (uint8)(secC[0] & 0x01u);
    if (mask == 0x80u)
    {
      mask = 0x01u;
      x++;
    }
    else
    {
      mask <<= 1;
    }

    secC[0] >>= 1;
    if ((secC[1] & 0x01u) != 0u)
    {
      secC[0] |= 0x80u;
    }
    secC[1] >>= 1;
    if ((secC[2] & 0x01u) != 0u)
    {
      secC[1] |= 0x80u;
    }

    secC[2] = (uint8)((secC[2] >> 1) | kSecB2[idx]);

    secC[0] ^= kSecC0[idx];
    secC[1] ^= kSecC1[idx];
    secC[2] ^= kSecC2[idx];
   }

  keyOutput[0]  = (uint8)((secC[0] >> 4) & 0x0Fu);
  keyOutput[0] |= (uint8)((secC[1] << 4) & 0xF0u);

  keyOutput[1]  = (uint8)((secC[2] >> 4) & 0x0Fu);
  keyOutput[1] |= (uint8)(secC[1] & 0xF0u);

  keyOutput[2]  = (uint8)(secC[2] & 0x0Fu);
  keyOutput[2] |= (uint8)((secC[0] << 4) & 0xF0u);

  return result;

}
uint8 SecurityAccess_CompareKey( uint8* key, uint8* KeyConstant, uint8* lastSeed )
{
  uint8      result;
  uint8*     computeVal;
  uint8      index;

  for (index = 0u; index < 3; index++)
  {
    computeVal[index] = 0u;
  }
  result = 0xFF;

    result = SecurityAccess_ComputeKey(lastSeed, KeyConstant, computeVal);
    for (index = 0u; index < 3u; index++)
    {
      if (computeVal[index] != key[index])
         {
            /* Comparison failed report failure */
            result = 0xFF;
         }
    }

  for (index = 0u; index < 3u; index++)
  {
    computeVal[index] = 0u;
  }

  return result;
} 
int main()
{
    printf("Hello, World:\n");
    uint8 fixBytes_05_06[5] = {0x41, 0xAA, 0x42, 0xBB, 0x43};
    uint8 seedBytes_1[3] = {0x1A, 0xF9, 0x64};
    uint8 seedBytes_2[3] = {0x4E, 0x96, 0x8A};

    uint8 keyArray[3] = {0x81,0x4B,0xA6};
    uint8 CompareKeyStatus_u8 = 0x12;

    CompareKeyStatus_u8 = SecurityAccess_CompareKey(keyArray,fixBytes_05_06,seedBytes_2);

    printf("%#X, ", CompareKeyStatus_u8);


return(0);
}

==============================================================================================
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

typedef unsigned char uint8;
typedef unsigned long uint32;
typedef unsigned long long uint64;

uint32 fix24 = 0xC541A9;
// get B21, B16, B13, B6, B4 bit data
/*
uint32 getValidBit()
{
return ((0x01 << 3) | (0x01 << 5) | (0x01 << 12) | (0x01 << 15) | (0x01 << 20));
}
*/
uint32 validBit = 0x109028;

void CalculateKeyArray(uint8 randomSeed[3], uint8 fixBytes[5], uint8 keyArray[3])
{
	uint64 challengeBit = 0;
	uint8 challengeBitArray[8] = {0x00};
	// copy seed and fix btyes to uint64 challengeBit
	memcpy(&(challengeBitArray[0]), &(randomSeed[0]), sizeof(uint8) * 3);
	memcpy(&(challengeBitArray[3]), &(fixBytes[0]), sizeof(uint8) * 5);
	memcpy(&challengeBit, &(challengeBitArray[0]), sizeof(challengeBitArray));
	//printf("\n%#lX\n", challengeBit);

	uint32 uintOne = 0x01;
	uint32 uintPosA = fix24;
	uint32 uintPosB = 0;
	uint32 uintPosC = 0;

	for (int i = 0; i < 64; ++i)
	{
		// B24 = A1 Xor CBx(CB1~CB64)
		uint32 uintA1 = uintPosA & uintOne;
		uint32 uintCBIndex = (challengeBit >> i) & uintOne;
		uint32 uintB24 = (uintA1 ^ uintCBIndex);

		uintPosB = (uintB24 << 23) | (uintPosA >> 1);

		// Position B Xor B24 to Position C
		uintPosC = (uintB24 == uintOne)? (uintPosB ^ validBit) : uintPosB;

		uintPosA = uintPosC;
	}

	//printf("%#X\n", uintPosC);
	// C12~C5
	uint32 uint32C12_C5 = uintPosC & 0x0FF0;
	keyArray[0] = uint32C12_C5 >> 4;
	// C16~C13 and C24~C21
	uint32 uint32C16_C13 = (uintPosC & 0xF000) >> 12;
	uint32 uint32C24_C21 = (uintPosC & 0xF00000) >> 20;
	keyArray[1] = (uint32C16_C13 << 4) | uint32C24_C21;
	// C4~C1 and C20~C17
	uint32 uint32C4_C1 = (uintPosC & 0x0F);
	uint32 uint32C20_C17 = (uintPosC & 0x0F0000) >> 16;
	keyArray[2] = (uint32C4_C1 << 4) | uint32C20_C17;
	printf("\n");
	// return keyArray;
}

int main()
{
	printf("Hello, World:\n");
	//uint8 fixBytes_05_06[5] = {0x41, 0xAA, 0x42, 0xBB, 0x43};
	uint8 fixBytes_05_06[5] =  {0x4Au, 0xDBu, 0x2Eu, 0xC5u, 0x35u};
	//uint8 seedBytes_1[3] = {0x1A, 0xF9, 0x64};
	uint8 seedBytes_2[3] = {0x4E, 0x96, 0x8A};
	uint8 keyArray[3] = {0x0,0x0,0x0};

	CalculateKeyArray(seedBytes_2, fixBytes_05_06, keyArray);
	for (int i = 0; i < 3; ++i)
	{
		printf("%#X, ", keyArray[i]);
	}

	return(0);
}
======================================================================================
// KeyGeneration.cpp : Defines the entry point for the DLL application.
//

#include <windows.h>
#include "KeyGenAlgoInterfaceEx.h"
#include "lib/hmac_sha_1.h"

typedef unsigned char uint8;
typedef unsigned long uint32;
typedef unsigned long long uint64;

static Esc_UINT8 SecurityAccess_ComputeKey_03_04(const Esc_UINT8 Seed[], Esc_UINT8 key[])
{
    Esc_UINT8 result = 0;

    const Esc_UINT8 K[8] = { 0x22, 0xD9, 0x83, 0x0A, 0x7A, 0x49, 0xC5, 0xD8 };
    EscHmacSha1_Calc(
        K,         /* key array               */
        8,          /* length of key in bytes  */
        Seed,     /* message array              */
        16,      /* length of message in bytes */
        key,               /* computed HMAC */
        16);

    return result;
}

BOOL APIENTRY DllMain( HANDLE hModule, 
                       DWORD  ul_reason_for_call, 
                       LPVOID lpReserved
					 )
{
    return TRUE;
}



KEYGENALGO_API VKeyGenResultEx GenerateKeyEx(
      const unsigned char*  iSeedArray,     /* Array for the seed [in] */
      unsigned int          iSeedArraySize, /* Length of the array for the seed [in] */
      const unsigned int    iSecurityLevel, /* Security level [in] */
      const char*           iVariant,       /* Name of the active variant [in] */
      unsigned char*        ioKeyArray,     /* Array for the key [in, out] */
      unsigned int          iKeyArraySize,  /* Maximum length of the array for the key [in] */
      unsigned int&         oSize           /* Length of the key [out] */
      )
{

    if (iSeedArraySize > iKeyArraySize)
    {
        return KGRE_BufferToSmall;
    }
#if 0
    for (unsigned int i=0;i<iSeedArraySize;i++)
      ioKeyArray[i]=~iSeedArray[i];
    oSize=iSeedArraySize;
#endif
#if 1
    uint8 result;
    uint8 idx, i;
    uint8 mask, x;
    uint8 secC[3], secF[8];

    uint8 kSecB2[2] = { 0x00u , 0x80u };
    uint8 kSecC2[2] = { 0x00u , 0x10u };
    uint8 kSecC1[2] = { 0x00u , 0x90u };
    uint8 kSecC0[2] = { 0x00u , 0x28u };

    /*Initialize local variable*/
    result = 0u;
    mask = 0x01u;
    x = 0u;

    secF[0] = iSeedArray[0];
    secF[1] = iSeedArray[1];
    secF[2] = iSeedArray[2];

    if (iSecurityLevel == 05)
    {
        //secF[3] = 0x9Au;
        //secF[4] = 0x2Bu;
        //secF[5] = 0x72u;
        //secF[6] = 0x1Eu;
        //secF[7] = 0x68u;
        secF[3] = 0x4Au;
        secF[4] = 0xDBu;
        secF[5] = 0x2Eu;
        secF[6] = 0xC5u;
        secF[7] = 0x35u;
    }
    else 
    {
        secF[3] = 0xFFu;
        secF[4] = 0xFFu;
        secF[5] = 0xFFu;
        secF[6] = 0xFFu;
        secF[7] = 0xFFu;
    }

    secC[0] = 0xA9u;
    secC[1] = 0x41u;
    secC[2] = 0xC5u;

    for (i = 0u; i < 64u; i++)
    {
        idx = (uint8)(((mask & secF[x]) != 0u) ? (1u) : (0u));

        idx ^= (uint8)(secC[0] & 0x01u);
        if (mask == 0x80u)
        {
            mask = 0x01u;
            x++;
        }
        else
        {
            mask <<= 1;
        }

        secC[0] >>= 1;
        if ((secC[1] & 0x01u) != 0u)
        {
            secC[0] |= 0x80u;
        }
        secC[1] >>= 1;
        if ((secC[2] & 0x01u) != 0u)
        {
            secC[1] |= 0x80u;
        }

        secC[2] = (uint8)((secC[2] >> 1) | kSecB2[idx]);

        secC[0] ^= kSecC0[idx];
        secC[1] ^= kSecC1[idx];
        secC[2] ^= kSecC2[idx];
    }

    ioKeyArray[0] = (uint8)((secC[0] >> 4) & 0x0Fu);
    ioKeyArray[0] |= (uint8)((secC[1] << 4) & 0xF0u);

    ioKeyArray[1] = (uint8)((secC[2] >> 4) & 0x0Fu);
    ioKeyArray[1] |= (uint8)(secC[1] & 0xF0u);

    ioKeyArray[2] = (uint8)(secC[2] & 0x0Fu);
    ioKeyArray[2] |= (uint8)((secC[0] << 4) & 0xF0u);

    oSize = iSeedArraySize;
#endif 
#if 0
    SecurityAccess_ComputeKey_03_04(iSeedArray, ioKeyArray);
    oSize = iSeedArraySize;
#endif
  return KGRE_Ok;
}



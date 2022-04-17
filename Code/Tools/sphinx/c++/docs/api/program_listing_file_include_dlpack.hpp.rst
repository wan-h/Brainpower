
.. _program_listing_file_include_dlpack.hpp:

Program Listing for File dlpack.hpp
===================================

|exhale_lsh| :ref:`Return to documentation for file <file_include_dlpack.hpp>` (``include/dlpack.hpp``)

.. |exhale_lsh| unicode:: U+021B0 .. UPWARDS ARROW WITH TIP LEFTWARDS

.. code-block:: cpp

   
   #ifndef DLPACK_DLPACK_H_
   #define DLPACK_DLPACK_H_
   
   #ifdef __cplusplus
   #define DLPACK_EXTERN_C extern "C"
   #else
   #define DLPACK_EXTERN_C
   #endif
   
   #define DLPACK_VERSION 60
   
   #define DLPACK_ABI_VERSION 1
   
   #ifdef _WIN32
   #ifdef DLPACK_EXPORTS
   #define DLPACK_DLL __declspec(dllexport)
   #else
   #define DLPACK_DLL __declspec(dllimport)
   #endif
   #else
   #define DLPACK_DLL
   #endif
   
   #include <stdint.h>
   #include <stddef.h>
   
   #ifdef __cplusplus
   extern "C" {
   #endif
   
   #ifdef __cplusplus
   typedef enum : int32_t {
   #else
   typedef enum {
   #endif
   
     kDLCPU = 1,
     kDLCUDA = 2,
     kDLCUDAHost = 3,
     kDLOpenCL = 4,
     kDLVulkan = 7,
     kDLMetal = 8,
     kDLVPI = 9,
     kDLROCM = 10,
     kDLROCMHost = 11,
     kDLExtDev = 12,
     kDLCUDAManaged = 13,
     kDLOneAPI = 14,
     kDLWebGPU = 15,
     kDLHexagon = 16,
   } DLDeviceType;
   
   typedef struct {
     DLDeviceType device_type;
     int32_t device_id;
   } DLDevice;
   
   typedef enum {
     kDLInt = 0U,
     kDLUInt = 1U,
     kDLFloat = 2U,
     kDLOpaqueHandle = 3U,
     kDLBfloat = 4U,
     kDLComplex = 5U,
   } DLDataTypeCode;
   
   typedef struct {
     uint8_t code;
     uint8_t bits;
     uint16_t lanes;
   } DLDataType;
   
   typedef struct {
     void* data;
     DLDevice device;
     int32_t ndim;
     DLDataType dtype;
     int64_t* shape;
     int64_t* strides;
     uint64_t byte_offset;
   } DLTensor;
   
   typedef struct DLManagedTensor {
     DLTensor dl_tensor;
     void * manager_ctx;
     void (*deleter)(struct DLManagedTensor * self);
   } DLManagedTensor;
   #ifdef __cplusplus
   }  // DLPACK_EXTERN_C
   #endif
   #endif  // DLPACK_DLPACK_H_

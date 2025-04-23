package com.yourcompany.scannerapp

import retrofit2.http.*
import retrofit2.Response

// DTO‑classes (maak in hetzelfde package of in models/)
data class ResourceDto(val id: String, val title: String)
data class WerkbonDto(
  val id: Int,
  val title: String,
  val start: String,
  val resourceId: String?,
  val barcode: String?,
  val client: String?
)
data class CreateWerkbonRequest(val title: String, val start: String, val resource: String)
data class CreateWerkbonResponse(val status: String, val id: Int)
data class UpdateWerkbonRequest(val start: String, val resourceId: String)
data class UpdateWerkbonResponse(val status: String)

// De interface met álle endpoints
interface ApiService {

  @GET("planning/api/resources/")
  suspend fun fetchResources(): List<ResourceDto>

  @GET("planning/api/werkbonnen/")
  suspend fun fetchWerkbonnen(
    @Query("start") start: String,
    @Query("end")   end:   String
  ): List<WerkbonDto>

  @POST("planning/api/werkbonnen/create/")
  suspend fun createWerkbon(@Body payload: CreateWerkbonRequest)
    : Response<CreateWerkbonResponse>

  @POST("planning/api/werkbonnen/{id}/update/")
  suspend fun updateWerkbon(
    @Path("id") id: Int,
    @Body payload: UpdateWerkbonRequest
  ): Response<UpdateWerkbonResponse>
}

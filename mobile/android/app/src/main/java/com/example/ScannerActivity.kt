package com.yourcompany.scannerapp

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.journeyapps.barcodescanner.CaptureActivity
import com.journeyapps.barcodescanner.ScanContract
import com.journeyapps.barcodescanner.ScanOptions
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

// Interface voor de API-calls (Retrofit)
interface ApiService {
    // Pas deze functie aan op jouw API (bijvoorbeeld: update de status van een werkbon)
    @retrofit2.http.POST("api/update_workbon/")
    fun updateWorkbon(@retrofit2.http.Body data: Map<String, Any>): Call<ApiResponse>
}

data class ApiResponse(val success: Boolean, val message: String)

class ScannerActivity : AppCompatActivity() {

    // Registreer de barcode scanner via de ZXing library
    private val barcodeLauncher = registerForActivityResult(ScanContract()) { result ->
        if(result.contents == null) {
            Toast.makeText(this, "Scan geannuleerd", Toast.LENGTH_LONG).show()
        } else {
            val scanResult = result.contents
            Toast.makeText(this, "Gescand: $scanResult", Toast.LENGTH_LONG).show()
            // Roep hier de functie aan om het resultaat naar je backend te sturen
            updateWorkbonStatus(scanResult)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_scanner)

        // Controleer of we camera-permissie hebben
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 0)
        } else {
            startScanning()
        }
    }

    private fun startScanning() {
        val options = ScanOptions().apply {
            setPrompt("Scan de QR-code van de werkbon")
            setBeepEnabled(true)
            setOrientationLocked(false)
            captureActivity = CaptureActivity::class.java
        }
        barcodeLauncher.launch(options)
    }

    // Callback voor resultaat van permissie
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 0 && grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            startScanning()
        } else {
            Toast.makeText(this, "Camera-toegang vereist voor scannen", Toast.LENGTH_LONG).show()
        }
    }

    // Functie om werkbonstatus te updaten via backend API (Retrofit)
    private fun updateWorkbonStatus(scanResult: String) {
        val data = mapOf("werkbon_id" to scanResult, "action" to "fase_afgerond")
        val apiService = ApiClient.getRetrofitInstance().create(ApiService::class.java)
        apiService.updateWorkbon(data).enqueue(object: Callback<ApiResponse> {
            override fun onResponse(call: Call<ApiResponse>, response: Response<ApiResponse>) {
                if (response.isSuccessful && response.body()?.success == true) {
                    Toast.makeText(this@ScannerActivity, "Werkbon status succesvol bijgewerkt", Toast.LENGTH_LONG).show()
                    finish()
                } else {
                    Toast.makeText(this@ScannerActivity, "Fout bij update: ${response.body()?.message}", Toast.LENGTH_LONG).show()
                }
            }
            override fun onFailure(call: Call<ApiResponse>, t: Throwable) {
                Toast.makeText(this@ScannerActivity, "Netwerkfout: ${t.localizedMessage}", Toast.LENGTH_LONG).show()
            }
        })
    }
}

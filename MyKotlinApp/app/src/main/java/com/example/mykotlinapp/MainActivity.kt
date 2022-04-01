package com.example.mykotlinapp

import android.content.Context
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import android.content.Intent
import android.widget.EditText
import okhttp3.*
import android.widget.Toast

import java.io.IOException

//import kotlinx.android.synthetic.main.list_item.*



const val EXTRA_MESSAGE = "com.example.mykotlinapp.MESSAGE"

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        val sharedPreferences = this.getSharedPreferences(
            "com.umar.restclient", Context.MODE_PRIVATE
        )
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // get reference to all views
        var et_user_name = findViewById(R.id.et_user_name) as EditText
        var et_password = findViewById(R.id.et_password) as EditText
        var btn_submit = findViewById(R.id.btn_submit) as Button



        // set on-click listener
        btn_submit.setOnClickListener {
            val user_name = et_user_name.text.toString();
            val password = et_password.text.toString();
            // send to check with database
            //val login = confirm_user(user_name, password)
            val login = 1;

            val intent = Intent(this, ThemeActivity::class.java)
            val intent_home = Intent(this, MainActivity::class.java)

            // val url = "https://homework5apad.uw.r.appspot.com/api/all_users"
            val url = "https://homework5apad.uw.r.appspot.com/api/check_pass/" + password + "/" + user_name

            val request = Request.Builder().url(url).build()
            val client = OkHttpClient()
            client.newCall(request).enqueue(object: Callback {

                override fun onResponse(call: Call, response: Response) {
                    val body = response.body?.string()
                    println(body)

                    val answer = body?.substring(10, 11)?.toInt()

                    //val gson = GsonBuilder().create()
                    //val checkUserFeed = gson.fromJson(body,Array<checkUserFeed>::class.java)
                    if (answer == 1){
                        startActivity(intent)
                        runOnUiThread {
                            Toast.makeText(
                                applicationContext,
                                "Welcome!",
                                Toast.LENGTH_LONG
                            ).show()
                        }

                    }
                    else {
                        runOnUiThread {
                            Toast.makeText(
                                applicationContext,
                                "Wrong username or password, try again!",
                                Toast.LENGTH_LONG
                            ).show()
                        }
                    }


//                    val userFeed =  gson.fromJson(body,Array<UserFeed>::class.java)
//                    println(userFeed)
//                    for (i in 0 until userFeed.count()) {
//                        // check email
//                        if (user_name == userFeed[i].email){
//                            if (password == userFeed[i].password){
//                                startActivity(intent)
//                                finish()
//                            }
//
//                        }
//                    }

                }
                override fun onFailure(call: Call, e: IOException) {
                    println("Failed to execute request")
                }
            })

        }


//            if (login == 1) {
//                val message = user_name;
//                val intent = Intent(this, ThemeActivity::class.java)
//                intent.putExtra("Message", message)
//                startActivity(intent)
//                finish()
//            } else {
//                Toast.makeText(
//                    this@MainActivity,
//                    "Wrong username or password, try again!",
//                    Toast.LENGTH_LONG
//                ).show()
//            }


        }
    }











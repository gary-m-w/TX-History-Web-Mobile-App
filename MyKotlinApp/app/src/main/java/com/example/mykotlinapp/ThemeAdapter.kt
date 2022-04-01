package com.example.mykotlinapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.course_detail_row.view.*


class ThemeAdapter(val themeFeed: Array<ThemeFeed>): RecyclerView.Adapter<ThemeViewHolder>() {
    override fun getItemCount(): Int {
        return themeFeed.count()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ThemeViewHolder {

        val layoutInflater = LayoutInflater.from(parent.context)
        val customView = layoutInflater.inflate(R.layout.course_detail_row, parent, false)
        return ThemeViewHolder(customView)
    }

    override fun onBindViewHolder(holder: ThemeViewHolder, position: Int) {
        val themedisplay = themeFeed.get(position)
        holder?.customView?.textView?.text = "Theme: "+themedisplay.label




        val thumbnailImageView = holder?.customView?.imageView2
        Picasso.get().load(themedisplay.cover).into(thumbnailImageView)



    }
}

    class  ThemeViewHolder(val customView: View): RecyclerView.ViewHolder(customView){
//        init {
//            customView.setOnClickListener{
//
//
//                val intent = Intent(customView.context,PostActivity::class.java)
//
//                customView.context.startActivity(intent)
//            }
//
//        }
    }

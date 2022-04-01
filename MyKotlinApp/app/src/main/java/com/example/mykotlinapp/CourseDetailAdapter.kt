package com.example.mykotlinapp

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.course_detail_row.view.*

class CourseDetailAdapter(val themeFeed: Array<ThemeFeed>): RecyclerView.Adapter<CourseLessonViewHolder>() {
    override fun getItemCount(): Int {
        return themeFeed.count()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): CourseLessonViewHolder {

        val layoutInflater = LayoutInflater.from(parent.context)
        val customView = layoutInflater.inflate(R.layout.course_detail_row, parent, false)
        return CourseLessonViewHolder(customView)
    }

    override fun onBindViewHolder(holder: CourseLessonViewHolder, position: Int) {
        val themedisplay = themeFeed.get(position)
        holder?.customView?.textView?.text = "Theme:"+themedisplay.label


        val thumbnailImageView = holder?.customView?.imageView2
        Picasso.get().load(themedisplay.cover).into(thumbnailImageView)



    }
}

class  CourseLessonViewHolder(val customView: View): RecyclerView.ViewHolder(customView){

}

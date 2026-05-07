SO yeah i was making face_to_anime but gotb overwhelmed by how much things i need to learn b4 making that hence wanted to work on something light and cool: `virtual joystick!`
So at first i wrote the basic code to track hand using mediapipe and wasn't sure how I can i do it excatly but we'll se later aayugewvfduy4ebfh

------------

The very first task I have to do now is to decide the controls. I have to make it confortable for player hence thinking to make it one hand only(left or right: what user is confortable in)

I think controls should be customizeable 
but for now I am making for **Minecraft**:
- WSAD - Hand forward, backward, left, right
- Left Click - Pinch thumb and index finger
- Rigt Click - Pinch thumb and middle finger
- Jump - Hand up
- Shift - Hand down
- Sprint - Hand Forward then rest then farward (under 1 sec)

There will also be a rest pose that keeps player in rest..
We might use other hand for config like for pause, for camera move change and other configs

------------

So after deciding controls, its time to implement! First task is to assign a rest pose of hand.
For this I used off hand: if it shows thumb up, the program will check, if main hand is present, if no so rest pose is blank or else it will check if all 21 landmarks of main hand is present, if yes, it will set the landmark of main hand as rest pose and will show in red.
I chose red color to differentiate from my live hands.

------------

It would be interesting - So my target was to measure the diff b/w rest_pose_hand ldms and current hand ldms so as to i can track the movement and do WASD, for this i had to firstly find out, what ldms we will use to find the diff first. At first i thought i should do of all ldms but that would be too much so i thought to use the center of hand.

For this i thought to find center of 0 - 12 and 4 - 20 then find the center of those both. I spent so much time to find the center and even did but didn't have idea on how to find center of those center point.. But soon i realized if we draw an imaginery line from 0-12 and 4-20, the intersection point will be center and when i did, it worked! but after spending hours, i realized 9 was close to the center, and my solution might be bad suppose if hand if lil bend but 9 will alays be near center and will stay at same place, hence i wasted my day

I also learned that sometime perfect is not what we need rather we need something that can work fast and reliably

-----------

It was pretty ez, i just had to find the diff between rest pose and crrenty hand ldm's. Though for threshold i was running my mind too much but it was simple
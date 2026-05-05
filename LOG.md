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
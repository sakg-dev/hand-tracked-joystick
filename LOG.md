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

------------

It was pretty ez, i just had to find the diff between rest pose and current hand ldm's. Though for threshold i was running my mind too much but it was simple

------------

python-uinput was already downloaded, just had to implement as shown in docs. Ran into some permission and module err but was working good at last. RIght now on every frame, it is pressing and releasing the key but eaglercraft(minecraft clone on browser) is not accepting it, afaik it might be either due to it is too fast that eaglercraft can't handle or eaglercraft is blocking it. 

So next time i may wanna try another module or trynna read more docs in it and see how i can keep it press until another key is not popped..

------------

So as i thought, eaglercraft was looking for press and release key instead of just click. At first i tried looking for something like that in python-uinput but there wasn't ig, so i moved to pynput which was surprisingly easier to work with as i didn't have to load uinput as well as it does the same thing press and release.

Then soon i implemented it and i was successfully able to do left, right, jump and sneak.

But there are some known issues and tasks:
 - The keys and mouse(input devices) doesn't work properly after i run pynput idk why, need to restart computer everytime i run it..
 - Rn it supports one key at a time only but we need combinations as well..
 - When i do right, it happens left and vice versa, i think i should flip the image 180 deg vertically to make it right, we'll see it later..

But b4 solving problems blindly, i should update readme with plans and everything and focus on what will make it work.

------------

So now we can do combinations as well! Just had to convert key from string to list and change some relevent code.

I think now i should focus on these issues: the input devices work weird after running the program and mirror

------------

So for quiting i saw it was occuring most of the time when i was switching window to shut it down and i guessed break was just breaking the loop not completely stopping it hence i added a gesture(thumb down in right hand) by which it will quit the program(most of the time it works but still buggy)

Mirroring was also ez, i just had to flip the img horizontally using cv2.flip

So now lets focus on depth! for forward and backward

------------

This was very interesting! So since i had to know the depth diff between rest pose hand and current hand, i had many ways to find it, i might have also utilized the z axis in landmark we get but i found it not that accurate then i thought i can measure the diameter(i donno if it is right word for polygonal) horizontally or vertically and then find the difference!
AT first i thought to use horizontal but soon realized it wouldn't be accurate as it changed dramatically if user stretches hand lil bit so decided to do vetically(0 and 12) which is much more stable.
Then after doing the same thing as i did with A and S, i was able to to W and S!

But till this point, just guessing the hand position and trynna move and see was so annoying, i wanted the cv screen on my screen while playing.
And most of the time, the input devices are no working when i try to shut down the program without keeping it in the rest pose..
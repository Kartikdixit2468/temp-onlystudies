from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class SceneTopic(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            GTTSService(
                lang="en",
                tld="com",

            )
        )
        
        with self.voiceover(text="Let's explore selection sort, a simple sorting algorithm."):
            title = Text("Selection Sort", font_size=60, color=YELLOW).to_edge(UP)
            self.play(Write(title))
            self.wait(2)
            self.play(FadeOut(title))
        
        with self.voiceover(text="Selection sort works by repeatedly finding the minimum element and placing it at the beginning."):
            
            # Create array elements
            values = [5, 2, 8, 1, 9, 4]
            squares = VGroup()
            for i, val in enumerate(values):
                sq = Square(side_length=1, color=BLUE)
                num = Text(str(val)).move_to(sq.get_center())
                group = VGroup(sq, num)
                squares.add(group)
            
            # Arrange nicely
            squares.arrange(RIGHT, buff=0.5)
            self.play(Create(squares))
            self.wait(1)
            
        with self.voiceover(text="We start by finding the smallest element in the unsorted portion."):
            # Find Minimum (Highlight)
            self.play(squares[0].animate.set_color(RED))
            self.play(squares[3].animate.set_color(GREEN))
            self.wait(1)
            self.play(squares[0].animate.set_color(BLUE), squares[3].animate.set_color(BLUE))
        
        with self.voiceover(text="Then, we swap it with the first element."):
            # Swap positions visually
            self.play(
                squares[0].animate.move_to(squares[3].get_center()),
                squares[3].animate.move_to(squares[0].get_center())
            )
            
            # Update VGroup list to match visual state
            squares.submobjects[0], squares.submobjects[3] = squares.submobjects[3], squares.submobjects[0]
            
            # Reset color
            self.play(squares[0].animate.set_color(BLUE), squares[3].animate.set_color(BLUE))
        
        with self.voiceover(text="Now we repeat, finding the next smallest element in the remaining unsorted portion."):
             # Find Minimum (Highlight)
            self.play(squares[1].animate.set_color(RED))
            self.play(squares[5].animate.set_color(GREEN))
            self.wait(1)
            self.play(squares[1].animate.set_color(BLUE), squares[5].animate.set_color(BLUE))

            # Swap positions visually
            self.play(
                squares[1].animate.move_to(squares[5].get_center()),
                squares[5].animate.move_to(squares[1].get_center())
            )
            
            # Update VGroup list to match visual state
            squares.submobjects[1], squares.submobjects[5] = squares.submobjects[5], squares.submobjects[1]
            
            # Reset color
            self.play(squares[1].animate.set_color(BLUE), squares[5].animate.set_color(BLUE))
        
        with self.voiceover(text="And swap it with the second element. This process continues until the entire array is sorted."):
             # Find Minimum (Highlight)
            self.play(squares[2].animate.set_color(RED))
            self.play(squares[4].animate.set_color(GREEN))
            self.wait(1)
            self.play(squares[2].animate.set_color(BLUE), squares[4].animate.set_color(BLUE))

            # Swap positions visually
            self.play(
                squares[2].animate.move_to(squares[4].get_center()),
                squares[4].animate.move_to(squares[2].get_center())
            )
            
            # Update VGroup list to match visual state
            squares.submobjects[2], squares.submobjects[4] = squares.submobjects[4], squares.submobjects[2]
            
            # Reset color
            self.play(squares[2].animate.set_color(BLUE), squares[4].animate.set_color(BLUE))
        
        with self.voiceover(text="Selection sort is simple to understand, but not very efficient for large datasets."):
            self.wait(2)
            self.play(FadeOut(squares))

        with self.voiceover(text="In summary, selection sort repeatedly finds the smallest element and puts it in its correct place."):
            summary = Text("Selection Sort: Find min, swap", font_size=48, color=GREEN)
            self.play(Write(summary))
            self.wait(2)
            self.play(FadeOut(summary))
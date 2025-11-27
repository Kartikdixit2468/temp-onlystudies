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

        # Introduction
        with self.voiceover(text="Let's explore matrix multiplication, a fundamental operation in linear algebra."):
            title = Text("Matrix Multiplication", font_size=60)
            self.play(Write(title))
            self.wait(2)
            self.play(FadeOut(title))
            self.wait(0.5)

        # Concept Explanation
        with self.voiceover(text="Matrix multiplication is not just element-wise. It involves taking the dot product of rows from the first matrix with columns from the second."):
            matrix_a = Matrix([[1, 2], [3, 4]])
            matrix_b = Matrix([[5, 6], [7, 8]])
            self.play(Create(matrix_a), Create(matrix_b))
            self.play(matrix_a.animate.shift(LEFT * 3), matrix_b.animate.shift(RIGHT * 3))
            self.wait(1)

        with self.voiceover(text="Each element in the resulting matrix is calculated by multiplying corresponding elements and summing the results."):
            arrow1 = CurvedArrow(matrix_a.get_rows()[0].get_left(), matrix_b.get_columns()[0].get_top(), angle = -PI/2)
            self.play(Create(arrow1))
            self.wait(1)
            self.play(FadeOut(arrow1))

        # Practical Example
        with self.voiceover(text="For example, let's multiply a 2x2 matrix by another 2x2 matrix."):
            resulting_matrix = Matrix([[19, 22], [43, 50]])
            self.play(matrix_a.animate.shift(LEFT * 3), matrix_b.animate.shift(RIGHT * 3), Write(Text("=", font_size = 50).move_to(ORIGIN)))
            self.play(Write(resulting_matrix.move_to(RIGHT * 3 + RIGHT * 3)))
            self.wait(1)

        with self.voiceover(text="The element in the first row and first column of the resulting matrix is obtained by multiplying 1 by 5, adding it to 2 multiplied by 7. That's 5 plus 14, which equals 19."):
            calculation = MathTex("(1*5) + (2*7) = 19").next_to(resulting_matrix, DOWN)
            self.play(Write(calculation))
            self.wait(2)
            self.play(FadeOut(calculation))

        # Conclusion
        with self.voiceover(text="So, that's matrix multiplication. It's a core concept for various applications in math, science, and engineering."):
            self.play(FadeOut(matrix_a), FadeOut(matrix_b), FadeOut(resulting_matrix))
            self.wait(1)

        with self.voiceover(text="Thank you for watching."):
            self.play(Write(Text("The End", font_size = 70)))
            self.wait(1)
            self.play(FadeOut(Text("The End", font_size = 70)))
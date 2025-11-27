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
        
        # 1. Introduction
        with self.voiceover(text="Today, we'll explore Dijkstra's algorithm, a powerful tool for finding the shortest path in a graph."):
            title = Text("Dijkstra's Algorithm", font_size=60, color=GREEN).scale(0.7)
            self.play(Write(title))
            self.wait(2)
            self.play(FadeOut(title))
        
        # 2. Concept Explanation
        with self.voiceover(text="Imagine a map with cities and roads. Dijkstra's algorithm helps us find the shortest route from one city to another."):
            # Create nodes (cities)
            nodes = [Dot(point=[i*2 - 3, np.sin(i), 0], color=BLUE, radius=0.2) for i in range(5)]
            labels = [Text(f"City {i+1}", font_size=24).next_to(nodes[i], DOWN, buff=0.1) for i in range(5)]
            
            # Create edges (roads) - manually set positions
            edges = [
                Line(nodes[0].get_center(), nodes[1].get_center(), color=WHITE),
                Line(nodes[0].get_center(), nodes[2].get_center(), color=WHITE),
                Line(nodes[1].get_center(), nodes[3].get_center(), color=WHITE),
                Line(nodes[2].get_center(), nodes[3].get_center(), color=WHITE),
                Line(nodes[3].get_center(), nodes[4].get_center(), color=WHITE),
                Line(nodes[2].get_center(), nodes[4].get_center(), color=WHITE),
            ]
            
            self.play(*[Create(node) for node in nodes], *[Write(label) for label in labels])
            self.play(*[Create(edge) for edge in edges])
            self.wait(1)
            
        with self.voiceover(text="It works by assigning a distance value to each city, starting with zero for the starting city and infinity for all others. It then iteratively updates these distances."):
            self.play(nodes[0].animate.set_color(GREEN), run_time=1)
            self.wait(2)
            
        # 3. Practical Example
        with self.voiceover(text="Let's walk through a simple example. We want to find the shortest path from City 1 to City 5. The algorithm explores neighboring cities, calculating distances. It keeps track of the shortest path found so far."):
            # Assign weights to the edges
            weights = [5, 2, 1, 4, 2, 6]
            weight_labels = []
            for i, edge in enumerate(edges):
                pos = edge.get_midpoint() + 0.2 * UP
                label = Text(str(weights[i]), font_size=20, color=YELLOW).move_to(pos)
                weight_labels.append(label)
            self.play(*[Write(label) for label in weight_labels])
            
            # Highlight path
            self.play(edges[0].animate.set_color(GREEN), weight_labels[0].animate.set_color(GREEN))
            self.play(edges[3].animate.set_color(GREEN), weight_labels[3].animate.set_color(GREEN))
            self.play(edges[4].animate.set_color(GREEN), weight_labels[4].animate.set_color(GREEN))
            self.wait(2)
            
        with self.voiceover(text="By repeatedly selecting the unvisited city with the smallest distance, Dijkstra's algorithm efficiently determines the shortest path to the destination."):
            self.play(nodes[4].animate.set_color(GREEN), run_time=1)
            self.wait(1)
            
        # 4. Conclusion
        with self.voiceover(text="In summary, Dijkstra's algorithm provides a systematic way to find the shortest path in a graph, making it useful in various applications, from GPS navigation to network routing."):
            self.play(*[FadeOut(mob) for mob in self.mobjects])
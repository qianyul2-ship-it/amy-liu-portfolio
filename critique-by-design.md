| [Home](README) | [Data Viz Examples](dataviz-examples) | [Critique by Design](critique-by-design) | [Final Project I](final-project-part-one) | [Final Project II](final-project-part-two) | [Final Project III](final-project-part-three) |

# Critique by Design: Taylor Swift's Album Releases and Tours

## Step one: Choose a visualization

I chose a Taylor Swift album and touring timeline featured in the MakeoverMonday **2026/W35: Taylor Swift Tours** challenge. The visualization originally appeared in Alice Zhao's *A Data Scientist Breaks Down All 10 Taylor Swift Albums* (March 2023), in a section discussing anticipation for The Eras Tour.

[Original article and visualization](https://adashofdata.com/2023/03/01/a-data-scientist-breaks-down-all-10-taylor-swift-albums-the-extended-version/)

I selected this visualization because the story is accessible and interesting even for readers who are not deeply familiar with Taylor Swift's career. The relationship between album releases and tours is inherently temporal, making it a useful opportunity to evaluate how visual placement communicates elapsed time. I wanted to retain the author's narrative about the unusual buildup to The Eras Tour while exploring whether the same information could be understood more quickly.

## Step two: Critique the original

I used Stephen Few's *Data Visualization Effectiveness Profile* to consider usefulness, completeness, perceptibility, truthfulness, intuitiveness, aesthetics, and engagement. I also applied the framework from Chapter 3 of *Good Charts*. I would classify the original as **data-driven and declarative**: it uses specific album and tour dates to communicate a preselected narrative about the anticipation surrounding The Eras Tour.

One strength is its use of album-associated colors, which makes the history recognizable and engaging for fans. Its chronological arrangement also gives readers a useful overview of how records and tours followed one another.

My central concern was **the perceptibility of elapsed time**. The story depends on the unusually long interval between the Reputation Tour and The Eras Tour, yet this comparison is not visually emphasized as strongly as it could be. Readers must inspect dates and annotations to infer the scale of the gap. For a declarative visualization, the main contrast should be immediately legible.

The title also goes beyond what the timeline can establish on its own. Album and tour histories provide plausible context for anticipation, but these data alone cannot measure ticket demand or prove its causes. In my redesign I therefore aim to make the *timeline evidence* more persuasive visually, while keeping this analytical limitation clear.

## Step three: Sketch a solution

My initial concept was a **dual-track, time-proportional horizontal timeline**: album releases above, tours below, both using the same continuous date scale. Equal distances on the horizontal axis would represent equal periods of time. Album-specific colors would preserve some of the personality of the original, while a highlighted interval would direct attention to the break between tours.

I also considered a more traditional timeline and an album-composition chart. I ultimately preferred the dual-track layout because it preserves the original purpose and enables a direct comparison of album releases with touring activity.

**Initial concept sketch:** The digital sketch below was generated with ChatGPT based on my proposed dual-track, time-proportional layout. It includes two tracks, a highlighted touring gap, and explanatory callouts. The final Tableau design simplifies this initial composition.

![Initial concept sketch of Taylor Swift album and tour timelines](images/taylor-swift-timeline-sketch.png)


## Step four: Test the solution

During the in-class critique, a specific piece of feedback on my digital sketch was that **the timeline appeared multiple times**, creating unnecessary repetition. The sketch included an album line, a tour line, and an additional year scale at the bottom. Although each element served a purpose, repeating the timeline made the overall layout feel more complicated and could distract viewers from the central comparison.

My response was to simplify the composition in Tableau. I retained the two meaningful data tracks, used a consistent continuous date scale, and removed the redundant third timeline. I also separated album releases (colored points) from tours (duration bars), so the two event types could be compared without relying on multiple repeated timelines. I used a reference band on both tracks to emphasize the interval between the Reputation Tour and The Eras Tour.

**Other peer responses:** [Add anonymized individual comments only if recorded or recalled from the classroom test. Do not include participants' names.]

**Synthesis:** The confirmed feedback reinforced a practical design trade-off: supplementary labels and axes can aid explanation, but repetition can weaken visual hierarchy. I prioritized a simpler, more readable presentation of the same chronological story.

## Step five: Build the solution in Tableau

I built the final redesign in **Tableau Public**, retaining the two horizontal tracks with a shared proportional date range. The upper track uses colored circles for studio-album release dates, and the lower track uses Gantt bars to show tour durations. Text labels identify tours, while the color legend identifies albums.

The original song-by-tour spreadsheet contained tour names, start and end dates, album names, and song titles, but it did not contain studio-album release dates. I supplemented it with album release dates for the ten studio albums available at the time of the 2023 article.

While building the chart, I discovered inconsistent dates for The Red Tour in the provided spreadsheet. Some rows placed it in 2011–2012, overlapping the Speak Now tour. I corrected those records to **March 13, 2013 through June 12, 2014** for the timeline and used the corrected dates to calculate tour durations.

I added a **reference band from November 21, 2018 to March 17, 2023**, showing the interval between the end of the Reputation Tour and the beginning of The Eras Tour. The exact between-tour interval is approximately four years and four months; describing 2018 to 2023 as five years is a year-to-year shorthand. During that period, *Lover*, *folklore*, *evermore*, and *Midnights* were released. Using this same highlighted period in both tracks makes the relationship between releases and the touring gap easier to see.

**Final Tableau visualization:** [Explore my interactive Tableau Public dashboard](https://public.tableau.com/app/profile/qianyu.liu/viz/TaylorSwiftToursRedesign/Dashboard1).

The most important change from the original is the use of **position and distance as explicit encodings of time**. The result is intended to help viewers perceive the gap directly and identify the four releases that preceded The Eras Tour. It offers historical context for anticipation while avoiding claims of causation that the underlying data cannot independently verify.

## References

- [MakeoverMonday, 2026/W35: Taylor Swift Tours](https://makeovermonday.co.uk/)
- [Alice Zhao, *A Data Scientist Breaks Down All 10 Taylor Swift Albums (The Extended Version)*, March 1, 2023](https://adashofdata.com/2023/03/01/a-data-scientist-breaks-down-all-10-taylor-swift-albums-the-extended-version/)
- Scott Berinato, *Good Charts*, Chapters 3–4.
- Stephen Few, *Data Visualization Effectiveness Profile*.
- Taylor Swift studio album release dates: [Add the specific reference consulted for the supplementary dates.]

## AI acknowledgements

I used ChatGPT as a brainstorming and technical support tool for this project. It helped me compare redesign approaches, articulate the critique, develop a preliminary digital concept sketch, and troubleshoot Tableau steps such as calculations, Gantt bars, labels, date axes, and reference bands. I constructed and refined the final visualization in Tableau Public. AI also assisted in drafting and editing the written reflection, which I reviewed against my design decisions and project work.

[Home](README) · [Data Viz Examples](dataviz-examples)

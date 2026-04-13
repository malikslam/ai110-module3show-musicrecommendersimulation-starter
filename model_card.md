# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatcher 1.0**

A simple content-based music recommender that matches songs to a user's taste profile by comparing numeric features and genres.  

---

## 2. Intended Use  

**What it does:** VibeMatcher suggests 5 songs from a small catalog that match a user's mood, energy level, and musical taste preferences.

**Who it's for:** This is a classroom learning tool only, not for real users. It's designed to explore how music recommenders work and where bias shows up.

**Key assumption:** The model assumes a user has one stable "vibe" at a time. It cannot recommend for users who want both relaxing and energetic tracks in the same session—they have to pick one profile.

**Not for:** Real music apps, production use, or large-scale recommendation. It's limited to 10 songs and simple features.  

---

## 3. How the Model Works  

**The idea:** For each song, calculate how well it matches the user's preferences. Give it a score from 0 to 1, where 1 is a perfect match. Recommend the top 5 highest-scoring songs.

**What we measure:**
- **Genre and mood:** Either they match exactly (score 1.0) or they don't (score 0.0). No in-between.
- **Energy, acousticness, momentum, valence, danceability:** The closer a song's value is to what the user wants, the higher the score. For example, if a user wants energy 0.8 and a song has 0.82, that gets a very high score.

**How we combine them:** We give different weights to different features. Mood is weighted 2x stronger than genre because it's a more direct signal of how a song feels. Energy is weighted 1.5x. We then average all the weighted scores to get a final number.

**Why this approach:** It's transparent and easy to explain. Users can see exactly why a song was recommended ("mood matched, energy is close").

---

## 4. Data  

**Catalog size:** 10 songs total—very small.

**Genres represented:** pop (2 songs), lofi (3 songs), rock (1), ambient (1), jazz (1), synthwave (1), indie pop (1).

**Moods:** happy, chill, intense, moody, relaxed, focused.

**Audio features:** Each song has energy (0–1), valence (0–1), danceability (0–1), acousticness (0–1), and tempo (60–152 BPM).

**What's missing:** The dataset is heavily biased. Lofi is overrepresented (30%), while rock, ambient, jazz, and synthwave are rare (10% each). There's no "ambient intense" song or "relaxed rock" song. Most songs are either upbeat pop or chill background music. Classical, heavy metal, country, and hip-hop are completely absent.

**Who does this reflect?** The data reflects Western indie/electronic/pop tastes. It does not represent global musical diversity.  

---

## 5. Strengths  

**Works well for:** Users with clear, single preferences. If someone says "I want chill lofi," the system nails it.

**Captures these patterns well:**
- High energy vs. chill energy. Profiles that prefer different energy levels get very different song lists, which makes sense.
- Acoustic vs. electronic. Users who prefer acoustic music see warm, guitar-heavy songs; those who prefer electronic see synths and production.
- Matching mood. If you ask for "happy" music, you get happy music. It's straightforward.

**When recommendations matched intuition:** For Profile A (Deep Intense Rock), Storm Runner ranked #1 with a score of 0.99. It's genuinely a perfect match—rock genre, intense mood, high energy, fast tempo. This felt obviously correct.

**Transparent explainability:** The system tells you *why* it recommended each song. "Genre matched (rock). Mood matched (intense). Energy is a close match (0.91)." Users can follow the logic.  

---

## 6. Limitations and Bias 

**Mood weight dominates genre preference, creating hidden filter bubbles.** During testing with the High-Energy Pop profile, I discovered that Rooftop Lights (indie pop, happy) ranked higher than Gym Hero (pop, intense), despite Gym Hero being an exact genre match. Both songs have similar energy (0.76 vs 0.93), but because mood is weighted 2.0 and genre only 1.0, indie pop's matching mood (happy) outweighed pop's exact genre match. This means users cannot reliably explore adjacent genres—if they want to discover music "similar to pop but with a different vibe," the system will never surface it competitively, even when all numeric features align. Real-world harm: users get locked into mood stereotypes within their favorite genres and never encounter cross-genre diversity, reinforcing echo chambers. The 10-song catalog amplifies this: underrepresented genres like ambient, jazz, and synthwave (one song each) are nearly invisible to users who don't explicitly prefer them, even if a song's numeric features are a perfect match.  

---

## 7. Evaluation  

I tested three distinct user profiles: **Profile A (Deep Intense Rock)**, **Profile B (High-Energy Pop)**, and **Profile C (Chill Lofi)**, spanning opposite ends of the energy spectrum and different genres.

**What I looked for:** I checked whether the #1 recommendation made sense for each profile, whether exact category matches (genre + mood) dominated, and whether numeric features (energy, tempo, acousticness) could compensate for a mismatch.

**What I found:**
- **Profile A (rock/intense)**: Storm Runner scored 0.99—perfect match on all 7 features. No surprises, exactly expected behavior.
- **Profile B (pop/happy)**: Sunrise City ranked #1 (0.98), which made sense. But Rooftop Lights (indie pop, happy) ranked #2, beating Gym Hero (pop, intense) at #3. *This surprised me*—I expected the exact genre match (pop) to dominate, but happy mood's 2.0 weight overwhelmed pop genre's 1.0 weight. This revealed the hidden bias in mood dominance.
- **Profile C (lofi/chill)**: Library Rain and Midnight Coding tied at 0.98—both are lofi/chill with nearly identical numeric features. This exposed a limitation: the system cannot distinguish between two songs that perfectly match a profile. It's an honest reflection of the data, not a bug, but it creates ties that feel boring.

**Surprise #1:** Mood weighting overwhelms genre—users looking for a specific genre with a different mood will never see it ranked highly.
**Surprise #2:** Small catalog gaps create impossible users—there's no "ambient intense" or "relaxed rock" song to recommend, so users with those combinations fall off a cliff in ranking.

---

## 8. Future Work  

**If I had more time, I would:**

1. **Add mood flexibility.** Allow users to input a mood *range* instead of a single value. "I want moods from relaxed to intense" so the system recommends varied tracks instead of locking users into one feeling.

2. **Lower mood's weight or make genre matching softer.** Right now mood dominates too much. I'd experiment with mood at 1.5 instead of 2.0, or allow "related genres" to score 0.5 instead of 0.0 (e.g., indie pop counts as a partial pop match).

3. **Expand the catalog significantly.** With 10 songs, rare genre combinations are impossible. Adding 50–100 songs would create real diversity and let the recommender handle users with unconventional tastes.

4. **Add a diversity toggle.** Instead of always returning the 5 highest-scoring songs, let users choose: "Give me all similar songs" or "Give me the most similar song from each genre." This fights filter bubbles.

5. **Support multiple user profiles for "group vibe."** "What should we all listen to together?" Right now it's designed for one person.  

---

## 9. Personal Reflection & Engineering Process

### Biggest Learning Moment

The biggest shock came when I ran Profile B (High-Energy Pop) and discovered Rooftop Lights beating Gym Hero in ranking. I had coded mood weight at 2.0 and genre weight at 1.0, but I didn't *feel* what that meant until I saw it in action. My algorithm did exactly what I told it to do—but what I told it to do had consequences I didn't anticipate. Mood became a tyrant. That moment made me understand that **the difference between a logically correct algorithm and a *fair* one is huge**. I was so focused on "does this match the user's preferences?" that I missed "does this limit what the user can discover?" Every weight, every threshold, every design choice is a values decision, not just a math decision.

### How AI Tools Helped (and When I Needed to Doubt Them)

**Where AI was invaluable:**
- **Explaining the weights.** When I used Copilot Inline Chat to ask "Why did Storm Runner score 0.99?", it traced through every feature and showed me the per-weight contribution. This visualization helped me understand my own code faster than I could have manually.
- **Identifying biases.** When I prompted Copilot to analyze my scoring logic for filter bubbles, it systematically found the mood lock-in problem, the genre scarcity amplification, and the danceability underweighting. It didn't miss things I would have overlooked.
- **Structuring the model card.** The template and examples helped me organize my thoughts into sections that made sense.

**Where I had to double-check or ignore AI:**
- **Weight selection.** Copilot suggested mood=2.0, energy=1.5, acousticness=1.5 initially. I should have questioned this more before implementing. In reality, these weights depend on domain knowledge I didn't have. I should have tested multiple weight configurations and chosen based on *fairness goals*, not just suggestions.
- **Code implementation details.** When Copilot generated the tempo normalization (divide by 200), I didn't question whether 200 was the right divisor. If songs over 200 BPM were added later, this would silently break. I should have documented this assumption or made it dynamic.
- **"This bias is not serious."** Early drafts of analysis said the bias was acceptable. I rejected this framing—bias is a design choice, not an inevitability. I had to push back and reframe the whole analysis.

### What Surprised Me About Simple Algorithms "Feeling" Like Recommendations

I expected my system to feel mechanical and obvious—like a spreadsheet sorting. Instead, it feels *intelligent*. When I see a ranked list with explanations ("mood matched, energy is close"), it creates an impression of understanding. My brain fills in gaps. If I don't see my favorite artist, I assume "the system doesn't know indie rock," not "the system has a bias I built in." This is dangerous. 

**The illusion of transparency:** Showing reasons ("why" it recommended) actually makes bias *harder* to detect, not easier. A user reads "mood matched (happy)" and thinks "oh, the system understands I like happy songs!" They don't think "the system weighted mood so high that it overrode my genre preference." Good explanations can be propaganda.

**Simplicity fools people into thinking it's fair.** A simple weighted average *feels* more trustworthy than a black-box neural network. But simplicity doesn't equal fairness—it just means the bias is easier for someone like me to spot if I debug it. Most users never debug. They just use it.

### What I Would Try Next

If I extended this project, I'd pursue two parallel paths:

**Path 1: Fairness-first redesign**
- Start by asking: "What types of users does this system serve well? Poorly?" Instead of optimizing for accuracy first, I'd optimize for *coverage*—every user type should get decent (not perfect, but decent) recommendations.
- Implement a "mood range" feature. Let users say "I want recommendations anywhere from chill to intense" instead of picking one spot.
- Add randomness or diversity to top-5 results. Don't just return highest scores; ensure at least one song from each genre if possible.

**Path 2: Scale and complexity**
- Expand to 1,000 songs and see where the algorithm breaks. Does it still handle edge cases? What new biases emerge?
- Add user clustering: "Users who like rock but enjoy jazz also tend to like..." to find unexpected cross-genre patterns without hard-coding them.
- Implement an A/B test: half users get accuracy-optimized weights, half get fairness-optimized weights. Measure which group discovers more music vs. gets more satisfied with recommendations.

**The deeper question I'd explore:** Is a "neutral" recommender possible? Or does every algorithm reflect the values and biases of whoever built it? I think it's the latter. The best I can do is be *honest* about the tradeoffs and let users opt into different philosophies: "Mode 1: Give me your perfect match. Mode 2: Surprise me. Mode 3: Challenge my taste."  

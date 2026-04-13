# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

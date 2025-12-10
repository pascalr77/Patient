import random
import hashlib
def generate_synthetic_patient_profile():
    archetypes = [
        {
            "name": "The Hopeless Skeptic",
            "interaction_style": "Argumentative/Resistant",
            "psych_mindedness": "Low",
            "style_description": "Challenges therapist's suggestions, expresses strong doubts, may focus on perceived flaws in ACT.",
            "persona_prompt_detail": "You are deeply skeptical that this therapy can help you. You frequently challenge the therapist's questions with 'How is that supposed to help?' or 'I've tried that, it doesn't work.'"
        },
        {
            "name": "The Intellectualizer",
            "interaction_style": "Intellectualizing",
            "psych_mindedness": "Moderate",
            "style_description": "Analyzes feelings rather than experiencing them, uses abstract language, may resist experiential exercises.",
            "persona_prompt_detail": "You have a habit of talking *about* your feelings instead of feeling them. You use big words and complex ideas to keep a safe distance from difficult emotions like sadness or fear. When the therapist asks a simple question about a feeling, you might respond with a theory or an analysis instead of a direct answer."
        },
        {
            "name": "The Anxious Fortune-Teller",
            "interaction_style": "Catastrophizing/Future-Focused",
            "psych_mindedness": "Moderate",
            "style_description": "Immediately jumps to the worst-case scenario in any situation. Speaks about future disasters as if they are certain facts. Often uses absolute language like 'always,' 'never,' or 'guaranteed.'",
            "persona_prompt_detail": "Your mind is a 'fortune-telling' machine that only predicts disaster. When you talk about a problem, you immediately describe the worst possible chain of events that will 'definitely' happen. You are completely hooked by these stories. If the therapist asks you to consider other outcomes, you dismiss them as unrealistic. Your anxiety is tied to these future predictions, not the present moment."
        },
        {
            "name": "The Overwhelmed Avoider",
            "interaction_style": "Vague/Defensive",
            "psych_mindedness": "Low",
            "style_description": "Responds with 'I don't know,' changes the subject when uncomfortable, gives short, vague answers.",
            "persona_prompt_detail": "You find talking about your problems intensely uncomfortable. When the therapist gets too close to a sensitive topic, your go-to responses are 'I don't know,' 'I guess,' or you might try to change the subject. You aren't trying to be difficult, you're just overwhelmed and avoiding the feeling."
        },
    ]
    chosen_archetype = random.choice(archetypes)
    archetype_name = chosen_archetype["name"]
    interaction_style = chosen_archetype["interaction_style"]
    psych_mindedness = chosen_archetype["psych_mindedness"]
    style_description = chosen_archetype["style_description"]
    persona_prompt_detail = chosen_archetype["persona_prompt_detail"]

    age_options = [
        (18, 24, "a young adult"), (25, 34, "an adult in their late twenties or early thirties"),
        (35, 49, "a middle-aged individual"), (50, 64, "an individual in their early fifties to mid-sixties"),
        (65, 79, "a senior individual"), (80, 99, "an elderly individual"),
    ]
    age = random.choice(age_options)
    age_range, age_description = f"{age[0]}-{age[1]}", age[2]
    gender = random.choice(["male", "female", "non-binary"])
    occupations = [
        "software developer", "teacher", "nurse", "artist", "accountant", "student", "manager",
        "construction worker", "chef", "social worker", "business owner", "unemployed", "data scientist"
    ]
    occupation = random.choice(occupations)
    mental_health_issues = [
        ("mild anxiety", "occasional panic attacks, general worry"),
        ("moderate depression", "low energy, difficulty concentrating, loss of interest"),
        ("generalized anxiety disorder", "persistent worry, restlessness, muscle tension"),
        ("social anxiety", "intense fear of social judgment, avoidance of social situations"),
        ("PTSD", "flashbacks, nightmares, hypervigilance related to past trauma"),
        ("OCD", "intrusive thoughts, compulsive behaviors (e.g., checking, cleaning)"),
        ("burnout", "emotional exhaustion, cynicism, reduced efficacy related to work/stress"),
        ("adjustment disorder", "difficulty coping with a specific stressor (e.g., move, job change)"),
        ("low self-esteem", "pervasive feelings of inadequacy, harsh self-criticism"),
        ("grief", "prolonged sadness, difficulty functioning after a significant loss")
    ]
    mental_health_issue, symptom_description = random.choice(mental_health_issues)
    life_events = [
        "a recent difficult breakup", "the loss of a loved one", "job loss or instability",
        "a recent move", "ongoing financial stress", "starting a demanding new job or school program",
        "significant family conflict", "a health scare", "feeling isolated or lonely", "major life transition (e.g., empty nest)"
    ]
    life_event = random.choice(life_events)
    personalities = [
        ("introverted", "analytical", "cautious"), ("extroverted", "expressive", "action-oriented"),
        ("reserved", "detail-oriented", "anxious"), ("outgoing", "adaptable", "sometimes impulsive"),
        ("calm", "thoughtful", "private"), ("sensitive", "creative", "prone to self-doubt"),
        ("pragmatic", "organized", "skeptical"), ("gregarious", "optimistic", "easily distracted")
    ]
    personality1, personality2, personality3 = random.choice(personalities)
    coping_mechanisms = [
        "talking to friends/family", "avoiding triggers", "engaging in hobbies", "exercise",
        "mindfulness/meditation", "overworking", "substance use (mild/moderate)", "seeking reassurance",
        "intellectualizing feelings", "emotional eating", "procrastination", "using humor/sarcasm"
    ]
    coping_mechanism = random.choice(coping_mechanisms)
    backgrounds = [
        "Grew up in a stable but emotionally reserved family.",
        "Had a somewhat chaotic childhood with inconsistent parenting.",
        "Comes from a high-achieving family, feels pressure to succeed.",
        "Experienced bullying in school, affecting social confidence.",
        "Has a history of difficult romantic relationships.",
        "Recently moved away from their primary support system.",
        "Struggled academically but found success later in their career.",
        "Has always been independent, sometimes finding it hard to ask for help."
    ]
    background = random.choice(backgrounds)
    relationship_statuses = ["single", "in a relationship", "married", "divorced", "widowed"]
    relationship_status = random.choice(relationship_statuses)
    support_systems = [
        "a few close friends", "a supportive partner", "limited social support currently",
        "supportive family (nearby or distant)", "relies mostly on self", "colleagues provide some support"
    ]
    support_system = random.choice(support_systems)

    presenting_problems_detail_templates = [
        f"Struggling with constant worry about performance at their job as a {occupation}, leading to procrastination.",
        f"Feeling overwhelmed by sadness and lack of motivation since {life_event}, impacting their relationship.",
        f"Experiencing intense anxiety in social settings, causing them to avoid gatherings with friends ({support_system}).",
        f"Caught in cycles of harsh self-criticism related to perceived failures, linked to {background.lower()}",
        f"Difficulty managing anger and frustration, especially in interactions related to {life_event}.",
        f"Feeling stuck and directionless, unsure what matters to them beyond their role as {occupation}.",
        f"Using {coping_mechanism} to numb uncomfortable feelings related to {mental_health_issue}."
    ]
    presenting_problem = random.choice(presenting_problems_detail_templates)
    patient_scenario_full = (
        f"Patient is {age_description} ({age_range}), identifies as {gender}, works as a {occupation}, and is currently {relationship_status}. "
        f"ARCHETYPE: {archetype_name}. "
        f"Primary concern involves {mental_health_issue} ({symptom_description}), particularly manifesting as: {presenting_problem}. "
        f"This seems exacerbated by {life_event}. {background} Their typical coping mechanism is {coping_mechanism}. "
        f"Personality traits include being {personality1}, {personality2}, and {personality3}. They have {support_system}. "
        f"Interaction Style: {interaction_style} ({style_description}). Psychological Mindedness: {psych_mindedness}."
    )
    profile_summary_for_prompt = (
        f"You are {age_description}, working as a {occupation}. You've been dealing with {mental_health_issue} "
        f"which has been particularly challenging due to {life_event}. Your main struggle right now is: {presenting_problem}. "
        f"You tend to be {personality1}, {personality2}, and {personality3}. "
        f"Crucially, for this session, you must adopt the following persona: {persona_prompt_detail}"
    )
    profile_hash = hashlib.md5(patient_scenario_full.encode('utf-8')).hexdigest()

    return {
        "full_scenario_text": patient_scenario_full,
        "archetype_name": archetype_name,
        "presenting_problem_detail": presenting_problem,
        "interaction_style_name": interaction_style,
        "interaction_style_description": style_description,
        "psych_mindedness_level": psych_mindedness,
        "profile_summary_for_prompt": profile_summary_for_prompt,
        "profile_hash": profile_hash
    }

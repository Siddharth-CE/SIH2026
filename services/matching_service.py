"""
Semantic Matching Service
Matches startups to challenges based on sector, core technology, keywords, capabilities, and past deployments.
Produces rich match breakdown and 'Why Matched' tags.
"""
from models import Startup, Challenge

def match_startups_for_challenge(challenge_id=None, challenge=None, min_score=40):
    """
    Computes match score and explanatory 'Why Matched' bullets for all eligible startups.
    """
    if not challenge and challenge_id:
        challenge = Challenge.query.get(challenge_id)
    
    if not challenge:
        return []

    # Keywords extracted from challenge title, problem, sector, constraints
    challenge_text = f"{challenge.title} {challenge.sector} {challenge.problem_summary} {challenge.technical_constraints or ''}".lower()
    
    all_startups = Startup.query.all()
    matches = []

    for startup in all_startups:
        score = 50 # Baseline baseline potential
        reasons = []

        # 1. Sector Alignment (+20)
        if startup.sector and (startup.sector.lower() in challenge.sector.lower() or challenge.sector.lower() in startup.sector.lower()):
            score += 20
            reasons.append(f"Direct Sector Match ({startup.sector})")
        elif any(w in challenge_text for w in (startup.sector or '').lower().split()):
            score += 10
            reasons.append("Cross-Sector Relevance")

        # 2. Technology & Capability Matches (+5 each up to 25)
        caps = startup.get_capabilities_list()
        matched_caps = []
        for cap in caps:
            if cap.lower() in challenge_text:
                score += 8
                matched_caps.append(cap)
        
        if matched_caps:
            reasons.append(f"Capabilities: {', '.join(matched_caps[:3])}")
        
        # Check core technology keywords
        tech_words = (startup.core_technology or '').lower().replace(',', ' ').split()
        matched_tech = [w.capitalize() for w in tech_words if len(w) > 3 and w in challenge_text]
        if matched_tech:
            score += 6
            reasons.append(f"Core Tech: {', '.join(list(set(matched_tech))[:3])}")

        # 3. Previous Deployment Experience (+15)
        if startup.deployments:
            gov_deployments = [d for d in startup.deployments if 'gov' in d.client_type.lower() or 'muni' in d.client_type.lower() or 'transit' in d.client_type.lower()]
            if gov_deployments:
                score += 12
                reasons.append(f"Proven Gov Deployment ({len(gov_deployments)} completed)")
            else:
                score += 5
                reasons.append(f"Enterprise Deployments ({len(startup.deployments)} references)")

        # 4. Trust & Compliance (+10)
        if startup.cybersecurity_certified:
            score += 6
            reasons.append(f"Security: {startup.cybersecurity_standard}")
        if startup.ip_ownership_clear:
            score += 4
            reasons.append("Full Proprietary IP Clearance")

        # Cap between 45 and 98
        score = min(98, max(45, score))

        if score >= min_score:
            matches.append({
                'startup': startup,
                'score': score,
                'reasons': reasons[:4],
                'is_top_match': score >= 85
            })

    # Sort descending by score
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches

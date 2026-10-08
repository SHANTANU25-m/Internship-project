import asyncio
from models.job import JobCreate
from services.job_service import save_search_results

raw_jd = """About the job
Who We Are
Notion is the collaborative AI workspace where teams and agents [think together](https://www.linkedin.com/safety/go/?url=https%3A%2F%2Fwww%2Eyoutube%2Ecom%2Fwatch%3Fv%3DvkpYpWfEK5s&urlhash=HHPl&mt=hc9z6QkZq2X11qfdg4qU2MnjAFFC99e6D72M9aSCtAKC94gQwdRaSEHWX7KA5b3mABt5u_4ZQ2SiBZbuQkv8_wDZ75A&isSdui=true). We're building one place where your knowledge, projects, meetings, and AI tools live side by side, so work is faster, clearer, and less fragmented. Millions of individuals, small teams, and large companies run their work on Notion.
Notinos (our employees) are customer zero in bringing this future of work to life. We care about craft, building things that last, and the belief that great work is still fundamentally human. Our goal isn’t to ship the next feature. Each and every team of Notinos is working to set the standard for how humans work together in the AI era. From building a business’s system of record to making and managing AI agents to automating away the busy work, we care deeply about giving our customers more time for their life’s work.
About The Role
We’re looking for an AI Applications Engineer to help drive Notion’s business transformation efforts. In this role, you’ll be a strategic partner to our internal stakeholders (primarily GTM, Finance and People teams) and deliver and scale creative AI-driven solutions to multi-faceted problems with measurable business impact. You’ll also build reusable components, evaluation patterns, and operational guardrails that make AI delivery repeatable across teams.
This role can be based in either San Francisco or New York City. We work from our offices on Mondays, Tuesdays and Thursdays (our Anchor Days) because we do our best thinking and building together in person. We’re looking for someone who’s excited to work alongside the team during those days.
What You’ll Achieve
• Work with stakeholders to discover opportunities from ambiguous problem statements, translate them into scoped solutions, and drive iterative releases from idea to adoption
• Build and ship end‑to‑end AI solutions—from problem framing through data readiness, modeling, evaluation, and production rollout
• Establish evaluation and production-readiness patterns (metrics, monitoring, human-in-the-loop, rollout plans) so solutions are reliable at scale
• Create reusable components, tooling, templates, and playbooks that accelerate future projects and enable other teams to ship safely
Skills You’ll Need To Bring
• 4-8 years of experience as a Software Engineer or Data Engineer (or equivalent), with a track record of building and operating production systems end-to-end across application code, data, and infrastructure. Domain experience partnering with GTM and Finance is a plus.
• Experience building AI-enabled applications in production (LLMs and/or classical ML), including prompt + tool orchestration, retrieval, evaluation, and iteration based on real-world feedback.
• Strong production-readiness instincts, including observability, monitoring, quality gates, incident response, and safe rollouts/rollbacks in live business workflows.
• Systems and integration fluency across APIs, data pipelines, and enterprise tools (e.g., CRM, finance, ticketing, HRIS), with the ability to navigate messy systems and still deliver reliable outcomes.
• Impact-driven approach to technology: You use technology to drive measurable user and business outcomes, not as an end in itself. You stay current with tools like Cursor, Claude Code, and other AI-assisted development environments, and you’re pragmatic about choosing what delivers the most value.
• Thoughtful problem-solving: You start with a clear understanding of context, align technical and non-technical partners, and translate AI concepts into actionable business outcomes. You navigate ambiguity and decompose complex problems into clean solutions.
• Empathetic communication and collaboration: You communicate nuanced ideas clearly and enjoy collaborating across engineering, data, and business teams.
• Familiarity with security, privacy, and governance for AI (access controls, PII handling, vendor/tool risk, auditability).
Notion is committed to providing highly competitive cash compensation, equity, and benefits. The compensation offered for this role will be based on multiple factors such as location, the role’s scope and complexity, and the candidate’s experience and expertise, and may vary from the range provided below. For roles based in San Francisco, the estimated base salary range for this role is $152,000 - $250,000 per year.
By clicking “Submit Application”, I understand and agree that Notion and its affiliates and subsidiaries will collect and process my information in accordance with Notion’s Global Recruiting Privacy Policy.
A Note on AI
You don’t need deep AI expertise for every role, but we do expect every Notino to be intellectually curious, drawn to tinkering and discovery, and excited to use AI as a real collaborator in their work. For some roles, AI fluency is a core requirement — when that’s the case, we'll say so explicitly in the qualifications. People who thrive here don’t treat AI as a novelty. They use it to think better, and make their work easier for others to build on.
Equal Opportunity & Accommodations
We hire talented people from a wide range of backgrounds. If you’re excited about this role but don’t meet every bullet, we still encourage you to apply. Notion is an equal opportunity employer and does not discriminate on the basis of any legally protected characteristic. Consistent with applicable law, we will consider for employment qualified applicants with arrest and conviction records. Notion provides reasonable accommodations during the application process; if you need one, please let your recruiter know.
"""

def run():
    job = JobCreate(
        title="AI Applications Engineer",
        company_name="Notion",
        location="San Francisco / New York City",
        description=raw_jd,
        job_url="https://notion.so/careers/ai-applications-engineer",  # mock url
        source="Manual Upload",
        salary_min=152000,
        salary_max=250000
    )
    
    save_search_results(
        keyword="AI Engineer",
        location="US",
        source="Manual",
        parsed_jobs=[job]
    )

if __name__ == "__main__":
    run()

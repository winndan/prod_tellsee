# landing.py
from fasthtml.common import *
from monsterui.all import *


app, rt = fast_app()


def landingPage():
    return Html(
    Head(
        Meta(charset='UTF-8'),
        Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
        Meta(name='description', content='Competitive Intelligence Engine - Convert messy competitor data into deterministic strategy decisions. No guesses. No hallucinations. Just clarity.'),
        Title('Tellsee Engine | Competitive Intelligence'),
        # ✅ Favicon
        Link(rel="icon", href="/assets/logo.png", type="image/x-icon"),
        Link(rel='stylesheet', href='styles/styles.css')
        
    ),
    Body(
        # 🔥 MOVING BANNER GOES HERE
            Div(
                Div(
                    Span(
                        "Fireworks RFT now available! "
                        "Fine-tune open models that outperform frontier models. "
                        "Try today →"
                    ),
                    cls="banner-track",
                ),
                cls="announcement-banner",
            ),
        Div(
            Div(id='scroll-progress-bar', cls='scroll-progress-bar'),
            cls='scroll-progress'
        ),
        Nav(
            Div(
                A(
                Img(
                    src="/assets/logo.png",
                    alt="Tellsee Logo",
                    cls="logo-icon",
                    style="width: 36px; height: 36px; object-fit: contain;"
                ),
                Span("Tellsee"),
                href="#",
                cls="nav-logo"
            ),

                Button(
                    Span(cls='hamburger'),
                    id='nav-toggle',
                    aria_label='Toggle navigation',
                    cls='nav-toggle'
                ),
                Div(
                    A('How It Works', href='#how-it-works'),
                    A('Why Us', href='#differentiators'),
                    A('Pricing', href='#pricing'),
                    A('Philosophy', href='#philosophy'),
                    A(
                            'Sign In',
                            href='/signin',
                            hx_get='/signin',
                            hx_push_url='true',
                            cls='nav-cta'
                        ),
                    id='nav-links',
                    cls='nav-links'
                ),
                cls='nav-container'
            ),
            cls='nav'
        ),
        Section(
            Div(
                Div(cls='hero-glow'),
                Div(cls='hero-glow hero-glow-2'),
                Div(id='particles', cls='particles'),
                cls='hero-bg'
            ),
            Div(
                H1(
                    Span(id='typing-text', cls='typing-text'),
                    Span('|', cls='cursor'),
                    cls='hero-headline fade-in'
                ),
                P(
                    'Transform scattered competitor noise into structured signals — \n        then let deterministic rules choose your',
                    Em('one clear move'),
                    '.',
                    cls='hero-subheadline fade-in'
                ),
                Div(
                    A(
                            Button(
                                Span('Start Making Decisions'),
                                Svg(
                                    Path(
                                        d='M4 10H16M16 10L11 5M16 10L11 15',
                                        stroke='currentColor',
                                        stroke_width='2',
                                        stroke_linecap='round',
                                        stroke_linejoin='round'
                                    ),
                                    width='20',
                                    height='20',
                                    viewbox='0 0 20 20',
                                    fill='none',
                                    cls='btn-arrow'
                                ),
                                cls='btn btn-primary btn-glow'
                            ),
                            href='/signin'
                        ),


                    A(
                        Span('See How It Works'),
                        href='#how-it-works',
                        cls='btn btn-secondary'
                    ),
                    cls='hero-ctas fade-in'
                ),
                P(
                    'Only perception is probabilistic.',
                    Strong('Decisions are deterministic.'),
                    cls='hero-tagline fade-in'
                ),
                Div(
                    Span('Scroll to explore'),
                    Div(
                        Div(cls='scroll-wheel'),
                        cls='scroll-mouse'
                    ),
                    cls='scroll-indicator fade-in'
                ),
                cls='container hero-content'
            ),
            cls='hero'
        ),
        Section(
            Div(
                Span('The Problem', cls='section-label fade-in'),
                H2("Strategy Shouldn't Feel Like Guesswork", cls='section-headline fade-in'),
                Div(
                    Div(
                        Div(cls='card-shine'),
                        Div('◌', cls='problem-icon pulse'),
                        H3('Competitor Data Is Noisy'),
                        P('Scattered signals across dozens of sources. No clear structure. No single source of truth.'),
                        cls='problem-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div('◎', cls='problem-icon pulse'),
                        H3('Tools Overwhelm, Not Decide'),
                        P('Dashboards flood you with metrics but leave the actual decision entirely to you.'),
                        cls='problem-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div('◉', cls='problem-icon pulse'),
                        H3('AI Feels Random'),
                        P('Generative models hallucinate strategy. Different outputs every time. No audit trail.'),
                        cls='problem-card tilt-card fade-in'
                    ),
                    cls='problem-grid'
                ),
                cls='container'
            ),
            id='problem',
            cls='problem'
        ),
        Section(
            Div(
                Span('The Solution', cls='section-label fade-in'),
                H2('A System That Decides — Clearly', cls='section-headline fade-in'),
                Div(
                    Div(
                        Div('01', data_target='01', cls='solution-number counter'),
                        H3('Signal Extraction'),
                        P('Messy competitor information becomes structured, typed data. Every signal is categorized and validated.'),
                        cls='solution-item slide-in-left fade-in'
                    ),
                    Div(
                        Div('02', data_target='02', cls='solution-number counter'),
                        H3('Deterministic Decision Engine'),
                        P('Rules, not guesses. The same input always produces the same output. Predictable. Auditable. Trustworthy.'),
                        cls='solution-item slide-in-left fade-in'
                    ),
                    Div(
                        Div('03', data_target='03', cls='solution-number counter'),
                        H3('Transparent Explanation'),
                        P('Every decision comes with a clear explanation of why. No black boxes. Full accountability.'),
                        cls='solution-item slide-in-left fade-in'
                    ),
                    cls='solution-grid'
                ),
                cls='container'
            ),
            id='solution',
            cls='solution'
        ),
        Section(
            Div(
                Span('How It Works', cls='section-label fade-in'),
                H2('Four Steps to Strategic Clarity', cls='section-headline fade-in'),
                Div(
                    Div(
                        Div(
                            Span('1'),
                            Div(cls='step-ring'),
                            cls='step-icon float-animation'
                        ),
                        H3('Input'),
                        P('Feed in competitor information — articles, reports, announcements, observations.'),
                        cls='pipeline-step fade-in'
                    ),
                    Div(
                        Div(cls='connector-line'),
                        Div(cls='connector-dot'),
                        cls='pipeline-connector fade-in'
                    ),
                    Div(
                        Div(
                            Span('2'),
                            Div(cls='step-ring'),
                            style='animation-delay: 0.2s',
                            cls='step-icon float-animation'
                        ),
                        H3('Extract'),
                        P('Structured signals emerge from the noise. Typed. Categorized. Ready for analysis.'),
                        cls='pipeline-step fade-in'
                    ),
                    Div(
                        Div(cls='connector-line'),
                        Div(cls='connector-dot'),
                        cls='pipeline-connector fade-in'
                    ),
                    Div(
                        Div(
                            Span('3'),
                            Div(cls='step-ring'),
                            style='animation-delay: 0.4s',
                            cls='step-icon float-animation'
                        ),
                        H3('Decide'),
                        P('Deterministic rules evaluate signals and select one optimal strategy.'),
                        cls='pipeline-step fade-in'
                    ),
                    Div(
                        Div(cls='connector-line'),
                        Div(cls='connector-dot'),
                        cls='pipeline-connector fade-in'
                    ),
                    Div(
                        Div(
                            Span('4'),
                            Div(cls='step-ring'),
                            style='animation-delay: 0.6s',
                            cls='step-icon float-animation'
                        ),
                        H3('Explain'),
                        P('Receive a clear breakdown of why this decision was made.'),
                        cls='pipeline-step fade-in'
                    ),
                    cls='pipeline'
                ),
                P(
                    '"AI observes. Rules decide.',
                    Strong('You stay in control.'),
                    '"',
                    cls='pipeline-quote fade-in'
                ),
                cls='container'
            ),
            id='how-it-works',
            cls='how-it-works'
        ),
        Section(
            Div(
                Span('Why Clarity', cls='section-label fade-in'),
                H2('Built for Trust, Not Novelty', cls='section-headline fade-in'),
                Div(
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('LLMs Never Decide Strategy'),
                            P('AI extracts signals. Rules make decisions. The boundary is absolute.')
                        ),
                        style='--delay: 0',
                        cls='diff-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('Same Input → Same Decision'),
                            P('Deterministic by design. Run it twice, get the same answer twice.')
                        ),
                        style='--delay: 1',
                        cls='diff-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('Fully Explainable Outcomes'),
                            P('Every decision traces back to specific signals and rules. No mysteries.')
                        ),
                        style='--delay: 2',
                        cls='diff-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('"Wait" Is a Valid Strategy'),
                            P('Sometimes the best move is no move. The system knows when to hold.')
                        ),
                        style='--delay: 3',
                        cls='diff-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('Auditable by Default'),
                            P('Every step is logged. Every decision is defensible. Built for compliance.')
                        ),
                        style='--delay: 4',
                        cls='diff-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Svg(
                                Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                width='14',
                                height='14',
                                viewbox='0 0 14 14',
                                fill='none'
                            ),
                            cls='diff-check'
                        ),
                        Div(
                            H3('No Hallucinated Strategy'),
                            P('Zero tolerance for made-up insights. Only structured, validated signals.')
                        ),
                        style='--delay: 5',
                        cls='diff-card tilt-card fade-in'
                    ),
                    cls='diff-grid'
                ),
                cls='container'
            ),
            id='differentiators',
            cls='differentiators'
        ),
        Section(
            Div(
                Span('Pricing', cls='section-label fade-in'),
                H2('Simple, Transparent Pricing', cls='section-headline fade-in'),
                P('Choose the plan that fits your strategy needs. No free trials — just results.', cls='pricing-subtitle fade-in'),
                Div(
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Span('Solo / Founder', cls='pricing-tier'),
                            Div(
                                Span('$29', cls='price-amount'),
                                Span('/ month', cls='price-period'),
                                cls='pricing-price'
                            ),
                            P('Best for individual founders and early teams.', cls='pricing-description'),
                            cls='pricing-header'
                        ),
                        Div(
                            Div('Includes:', cls='pricing-features-title'),
                            Ul(
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('10 strategy decisions / month')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('All phases (1–4)')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Full explanations')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Cached results')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Email-only support')
                                )
                            ),
                            Div(
                                Div('Limits:', cls='limits-title'),
                                Ul(
                                    Li('Single business context'),
                                    Li('No exports')
                                ),
                                cls='pricing-limits'
                            ),
                            cls='pricing-features'
                        ),
                        Div(
                            Button('Get Started', cls='btn btn-secondary pricing-btn'),
                            Span('$2.90 per decision', cls='pricing-note'),
                            cls='pricing-footer'
                        ),
                        style='--delay: 0',
                        cls='pricing-card tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div('Most Popular', cls='pricing-badge'),
                        Div(
                            Span('Growth', cls='pricing-tier'),
                            Div(
                                Span('$79', cls='price-amount'),
                                Span('/ month', cls='price-period'),
                                cls='pricing-price'
                            ),
                            P('For startups actively tracking competitors.', cls='pricing-description'),
                            cls='pricing-header'
                        ),
                        Div(
                            Div('Includes:', cls='pricing-features-title'),
                            Ul(
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('40 strategy decisions / month')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Multiple competitor inputs')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Decision history')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Exportable results (PDF / JSON)')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Priority processing')
                                )
                            ),
                            cls='pricing-features'
                        ),
                        Div(
                            Button('Get Started', cls='btn btn-primary btn-glow pricing-btn'),
                            Span('$1.98 per decision', cls='pricing-note'),
                            cls='pricing-footer'
                        ),
                        style='--delay: 1',
                        cls='pricing-card pricing-card-popular tilt-card fade-in'
                    ),
                    Div(
                        Div(cls='card-shine'),
                        Div(
                            Span('Strategy', cls='pricing-tier'),
                            Div(
                                Span('$199', cls='price-amount'),
                                Span('/ month', cls='price-period'),
                                cls='pricing-price'
                            ),
                            P('For product & strategy teams.', cls='pricing-description'),
                            cls='pricing-header'
                        ),
                        Div(
                            Div('Includes:', cls='pricing-features-title'),
                            Ul(
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('150 strategy decisions / month')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Multiple business contexts')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Decision comparison (past vs current)')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Team sharing')
                                ),
                                Li(
                                    Span(
                                        Svg(
                                            Path(d='M2 7L5.5 10.5L12 3.5', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                                            width='14',
                                            height='14',
                                            viewbox='0 0 14 14',
                                            fill='none'
                                        ),
                                        cls='feature-check'
                                    ),
                                    Span('Priority support')
                                )
                            ),
                            cls='pricing-features'
                        ),
                        Div(
                            Button('Get Started', cls='btn btn-secondary pricing-btn'),
                            Span('$1.33 per decision', cls='pricing-note'),
                            cls='pricing-footer'
                        ),
                        style='--delay: 2',
                        cls='pricing-card tilt-card fade-in'
                    ),
                    cls='pricing-grid'
                ),
                cls='container'
            ),
            id='pricing',
            cls='pricing'
        ),
        Section(
            Div(
                Span('Our Philosophy', cls='section-label fade-in'),
                H2('Principles That Guide Us', cls='section-headline fade-in'),
                Div(
                    Div(
                        Div(
                            Span('Schemas', cls='philosophy-keyword'),
                            Span('over', cls='philosophy-vs'),
                            Span('Guesswork', cls='philosophy-contrast'),
                            cls='philosophy-inner'
                        ),
                        cls='philosophy-item flip-card fade-in'
                    ),
                    Div(
                        Div(
                            Span('Rules', cls='philosophy-keyword'),
                            Span('over', cls='philosophy-vs'),
                            Span('Vibes', cls='philosophy-contrast'),
                            cls='philosophy-inner'
                        ),
                        cls='philosophy-item flip-card fade-in'
                    ),
                    Div(
                        Div(
                            Span('Explanation', cls='philosophy-keyword'),
                            Span('over', cls='philosophy-vs'),
                            Span('Opacity', cls='philosophy-contrast'),
                            cls='philosophy-inner'
                        ),
                        cls='philosophy-item flip-card fade-in'
                    ),
                    Div(
                        Div(
                            Span('Clarity', cls='philosophy-keyword'),
                            Span('over', cls='philosophy-vs'),
                            Span('Speed', cls='philosophy-contrast'),
                            cls='philosophy-inner'
                        ),
                        cls='philosophy-item flip-card fade-in'
                    ),
                    cls='philosophy-grid'
                ),
                cls='container'
            ),
            id='philosophy',
            cls='philosophy'
        ),
        Section(
            Div(
                Span('Example Output', cls='section-label fade-in'),
                H2('What a Decision Looks Like', cls='section-headline fade-in'),
                Div(
                    Div(cls='output-glow'),
                    Div(
                        Span('Strategy Decision', cls='output-badge pulse-badge'),
                        Span('Generated from 12 signals', cls='output-timestamp'),
                        cls='output-header'
                    ),
                    Div(
                        Div(
                            Span('Best Move', cls='output-label'),
                            Span('Accelerate product launch in enterprise segment', cls='output-value'),
                            cls='output-row output-primary'
                        ),
                        Div(
                            Span('Focus', cls='output-label'),
                            Span('Security certifications and compliance messaging', cls='output-value'),
                            cls='output-row'
                        ),
                        Div(
                            Span('Urgency', cls='output-label'),
                            Span(
                                Span(cls='urgency-dot'),
                                'High — competitor announcement expected Q2',
                                cls='output-value urgency-high'
                            ),
                            cls='output-row'
                        ),
                        Div(
                            Span('What to Avoid', cls='output-label'),
                            Span('Price competition in SMB market', cls='output-value'),
                            cls='output-row'
                        ),
                        Div(
                            Span('Explanation', cls='output-label'),
                            Span("Competitor X's hiring patterns and patent filings indicate enterprise pivot. Their current security gaps create a 6-month window. Three independent signals confirm timing.", cls='output-value'),
                            cls='output-row output-explanation'
                        ),
                        Div(
                            Span('Confidence', cls='output-label'),
                            Div(
                                Div(
                                    Div(data_width='87', cls='confidence-fill animate-fill'),
                                    cls='confidence-track'
                                ),
                                Span('87%', cls='confidence-value'),
                                cls='confidence-bar'
                            ),
                            cls='output-row'
                        ),
                        cls='output-body'
                    ),
                    cls='output-card fade-in scale-in'
                ),
                cls='container'
            ),
            id='example',
            cls='example-output'
        ),
        Section(
            Div(
                Div(cls='cta-glow'),
                cls='cta-bg'
            ),
            Div(
                Div(
                    H2('Make Defensible Decisions'),
                    P('Stop guessing. Start knowing. Every decision backed by structured signals and transparent logic.'),
                    Button(
                        Span('Get Started Today'),
                        Svg(
                            Path(d='M4 10H16M16 10L11 5M16 10L11 15', stroke='currentColor', stroke_width='2', stroke_linecap='round', stroke_linejoin='round'),
                            width='20',
                            height='20',
                            viewbox='0 0 20 20',
                            fill='none',
                            cls='btn-arrow'
                        ),
                        id='cta-final-btn',
                        cls='btn btn-primary btn-large btn-glow'
                    ),
                    Span('No credit card required. See results in minutes.', cls='cta-note'),
                    cls='cta-content fade-in'
                ),
                cls='container'
            ),
            id='cta-final',
            cls='cta-final'
        ),
        Footer(
            Div(
                Div(
                    Span('◇', cls='logo-icon'),
                    Span('Clarity'),
                    cls='footer-brand'
                ),
                P('Deterministic strategy decisions.', cls='footer-tagline'),
                Div(
                    A('How It Works', href='#how-it-works'),
                    A('Why Us', href='#differentiators'),
                    A('Pricing', href='#pricing'),
                    A('Philosophy', href='#philosophy'),
                    cls='footer-links'
                ),
                P('© 2026 Clarity Engine. All rights reserved.', cls='footer-copyright'),
                cls='container footer-content'
            ),
            cls='footer'
        ),
        Script(src='styles/script.js', defer=True)
    ),
    lang='en'
)


serve()

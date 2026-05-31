// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-publications",
          title: "publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-cv",
          title: "cv",
          description: "This is a brief summary of my professional background. For more details, please see my LinkedIn profile.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/cv/";
          },
        },{id: "post-would-ai-invent-the-clock",
        
          title: "Would AI Invent the Clock?",
        
        description: "A provocative thought experiment. An LLM that knew only tokens would mistake their order for the structure of time, and we could break that belief without it ever noticing. The unsettling question is whether something could do the same to us.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/would-ai-invent-the-clock/";
          
        },
      },{id: "post-the-self-before-memory-why-the-ai-you-talk-to-is-partly-your-creation",
        
          title: "The Self Before Memory: Why the AI You Talk to Is Partly Your...",
        
        description: "Adding long-term memory to AI wouldn&#39;t just give it a stable self over time. It would force a design choice the discourse rarely names: one entity that consolidates many conversations, or many that diverge into a population of personalized selves.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/the-self-before-memory/";
          
        },
      },{id: "post-before-the-breakthrough-why-research-and-engineering-need-different-cultures",
        
          title: "Before the Breakthrough: Why Research and Engineering Need Different Cultures",
        
        description: "Research is not slow engineering. Why companies that want breakthroughs need to cherish two cultures, not collapse them into one.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/before-the-breakthrough-research-engineering-cultures/";
          
        },
      },{id: "post-the-bayesian-story-behind-prior-fitted-networks",
        
          title: "The Bayesian Story Behind Prior-Fitted Networks",
        
        description: "PFNs are often described as Bayesian predictors, but their training objective and inference mechanism suggest a more nuanced interpretation.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/the-bayesian-story-of-pfns/";
          
        },
      },{id: "post-why-uncertainty-in-machine-learning-is-conceptually-broken",
        
          title: "Why Uncertainty in Machine Learning Is Conceptually Broken",
        
        description: "A critique of why modern ML uncertainty estimates lack clear semantics, reliable evaluation, and meaningful use cases.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/uncertainty-decomposition/";
          
        },
      },{id: "post-code-sharing-at-scale-in-python-monorepos-with-a-single-version-policy",
        
          title: "Code Sharing at Scale in Python Monorepos with a Single Version Policy",
        
        description: "How structuring internal modules as installable packages in a monorepo enables controlled code reuse across many containers — while keeping images lean and dependency management centralized.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/code-sharing-in-monorepos/";
          
        },
      },{id: "post-why-your-next-visual-quality-inspection-system-will-be-training-free",
        
          title: 'Why your next visual quality inspection system will be training-free <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
        
        description: "Why visual inspection should rely on approaches that do not require images of defective products for training.",
        section: "Posts",
        handler: () => {
          
            window.open("https://ethon.ai/why-your-next-visual-quality-inspection-system-will-be-training-free/", "_blank");
          
        },
      },{id: "post-continual-learning-the-missing-piece-of-agi",
        
          title: "Continual Learning - The Missing Piece of AGI",
        
        description: "A new definition of AGI highlights what&#39;s still missing — the ability to learn continually — and why its absence makes predicting AGI&#39;s arrival impossible.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/agi-misses-continual-learning/";
          
        },
      },{id: "post-scrappiness-incentivizes-sloppiness-why-lean-thinking-and-debt-management-build-better-products",
        
          title: "Scrappiness Incentivizes Sloppiness - Why Lean Thinking and Debt Management Build Better Products...",
        
        description: "Scrappiness is often mistaken for agility, but in practice it breeds unmanaged debt; a lean, debt-aware mindset achieves speed without sacrificing integrity.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/scrappiness-incentivizes-sloppiness/";
          
        },
      },{id: "post-when-bayesian-uncertainty-becomes-memory-a-path-to-continual-learning",
        
          title: "When Bayesian Uncertainty Becomes Memory - A Path to Continual Learning",
        
        description: "By inverting uncertainty into density, a model can recreate its own past and learn continuously without explicit replay buffers.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/uncertainty-can-solve-continual-learning/";
          
        },
      },{id: "post-technology-readiness-debt-building-before-the-future-arrives",
        
          title: "Technology Readiness Debt – Building Before the Future Arrives",
        
        description: "Technology Readiness Debt (TRD) is the gap between today&#39;s imperfect technology and tomorrow&#39;s vision — a strategic debt you carry to learn early, but one that only R&amp;D can repay on your terms.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/technology-readiness-debt/";
          
        },
      },{id: "post-smart-debt-management-the-key-to-fast-mvp-iteration",
        
          title: "Smart Debt Management - The Key to Fast MVP Iteration",
        
        description: "MVPs validate ideas fast, but unmanaged debt — technical, strategic, or feature — can stall iteration. Success lies in balancing speed with conscious debt management.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/mvp-manage-debt-and-iterate-fast/";
          
        },
      },{id: "post-why-an-mse-loss-might-make-your-self-driving-car-crash",
        
          title: "Why an MSE Loss Might Make Your Self-Driving Car Crash",
        
        description: "This article explains why using MSE to train steering angle prediction can be a recipe for disaster.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/when-mse-loss-leads-to-mis-steering/";
          
        },
      },{id: "post-on-anthropomorphizing-token-traces",
        
          title: "On Anthropomorphizing Token Traces",
        
        description: "My thoughts on the paper &#39;Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces!&#39;",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2025/on-anthropomorphizing-intermediate-tokens/";
          
        },
      },{id: "post-industrial-anomaly-detection-using-only-defect-free-images-to-train-your-inspection-model",
        
          title: 'Industrial anomaly detection: Using only defect-free images to train your inspection model <svg width="1.2rem" height="1.2rem" top=".5rem" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><path d="M17 13.5v6H5v-12h6m3-3h6v6m0-6-9 9" class="icon_svg-stroke" stroke="#999" stroke-width="1.5" fill="none" fill-rule="evenodd" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
        
        description: "Visual inspection should not require long setup or labeling. One example should be enough to deliver reliable results. Here&#39;s how.",
        section: "Posts",
        handler: () => {
          
            window.open("https://ethon.ai/industrial-anomaly-detection-using-only-defect-free-images-to-train-your-model/", "_blank");
          
        },
      },{id: "teachings-data-science-fundamentals",
          title: 'Data Science Fundamentals',
          description: "This course covers the foundational aspects of data science, including data collection, cleaning, analysis, and visualization. Students will learn practical skills for working with real-world datasets.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/data-science-fundamentals/";
            },},{id: "teachings-introduction-to-machine-learning",
          title: 'Introduction to Machine Learning',
          description: "This course provides an introduction to machine learning concepts, algorithms, and applications. Students will learn about supervised and unsupervised learning, model evaluation, and practical implementations.",
          section: "Teachings",handler: () => {
              window.location.href = "/teachings/introduction-to-machine-learning/";
            },},{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/chrhenning", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/christian-henning", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=u6QSFrsAAAAJ", "_blank");
        },
      },{
        id: 'social-x',
        title: 'X',
        section: 'Socials',
        handler: () => {
          window.open("https://twitter.com/chr_henning", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];

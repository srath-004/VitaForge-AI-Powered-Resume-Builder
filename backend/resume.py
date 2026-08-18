import React, { useMemo, useState } from "react";
import "./App.css";

const emptyProject = {
  title: "",
  technologies: "",
  description: "",
};

const emptyExperience = {
  company: "",
  role: "",
  duration: "",
  description: "",
};

const App = () => {
  const [resumeData, setResumeData] = useState({
    name: "",
    email: "",
    phone: "",
    location: "",
    linkedin: "",
    github: "",
    fontFamily: "font-calibri",
    fontWeight: "normal",
    role: "",
    summary: "",

    degree: "",
    college: "",
    cgpa: "",
    year: "",

    programming: "",
    coreSkills: "",
    tools: "",
    databases: "",
    softSkills: "",

    projects: [
      { ...emptyProject },
      { ...emptyProject },
    ],

    experiences: [
      { ...emptyExperience },
    ],

    certifications: "",

    jd: "",
  });

  /* =====================================================
     GENERAL INPUT HANDLER
  ===================================================== */

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    setResumeData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  /* =====================================================
     PROJECT HANDLER
  ===================================================== */

  const handleProjectChange = (index, field, value) => {
    setResumeData((prev) => {
      const projects = [...prev.projects];

      projects[index] = {
        ...projects[index],
        [field]: value,
      };

      return {
        ...prev,
        projects,
      };
    });
  };

  const addProject = () => {
    setResumeData((prev) => ({
      ...prev,
      projects: [
        ...prev.projects,
        { ...emptyProject },
      ],
    }));
  };

  const removeProject = (index) => {
    setResumeData((prev) => ({
      ...prev,
      projects: prev.projects.filter(
        (_, i) => i !== index
      ),
    }));
  };

  /* =====================================================
     EXPERIENCE HANDLER
  ===================================================== */

  const handleExperienceChange = (
    index,
    field,
    value
  ) => {
    setResumeData((prev) => {
      const experiences = [...prev.experiences];

      experiences[index] = {
        ...experiences[index],
        [field]: value,
      };

      return {
        ...prev,
        experiences,
      };
    });
  };

  const addExperience = () => {
    setResumeData((prev) => ({
      ...prev,
      experiences: [
        ...prev.experiences,
        { ...emptyExperience },
      ],
    }));
  };

  const removeExperience = (index) => {
    setResumeData((prev) => ({
      ...prev,
      experiences: prev.experiences.filter(
        (_, i) => i !== index
      ),
    }));
  };

  /* =====================================================
     RESUME COMPLETION
  ===================================================== */

  const completion = useMemo(() => {
    const fields = [
      resumeData.name,
      resumeData.email,
      resumeData.phone,
      resumeData.location,
      resumeData.role,
      resumeData.summary,
      resumeData.degree,
      resumeData.college,
      resumeData.cgpa,
      resumeData.year,
      resumeData.programming,
      resumeData.coreSkills,
      resumeData.tools,
      resumeData.databases,
      resumeData.softSkills,
      resumeData.certifications,
    ];

    let filled = fields.filter(
      (field) =>
        field &&
        field.toString().trim().length > 0
    ).length;

    resumeData.projects.forEach((project) => {
      if (project.title.trim()) filled++;
      if (project.description.trim()) filled++;
    });

    resumeData.experiences.forEach((experience) => {
      if (experience.company.trim()) filled++;
      if (experience.description.trim()) filled++;
    });

    const total =
      fields.length +
      resumeData.projects.length * 2 +
      resumeData.experiences.length * 2;

    return Math.min(
      100,
      Math.round((filled / total) * 100)
    );
  }, [resumeData]);

  /* =====================================================
     ATS SCORE
  ===================================================== */

  const atsAnalysis = useMemo(() => {
    const resumeText = `
      ${resumeData.name}
      ${resumeData.role}
      ${resumeData.summary}
      ${resumeData.degree}
      ${resumeData.college}
      ${resumeData.programming}
      ${resumeData.coreSkills}
      ${resumeData.tools}
      ${resumeData.databases}
      ${resumeData.softSkills}
      ${resumeData.certifications}
      ${resumeData.projects
        .map(
          (p) =>
            `${p.title} ${p.technologies} ${p.description}`
        )
        .join(" ")}
      ${resumeData.experiences
        .map(
          (e) =>
            `${e.company} ${e.role} ${e.description}`
        )
        .join(" ")}
    `.toLowerCase();

    const jdText = resumeData.jd.toLowerCase();

    if (!jdText.trim()) {
      return {
        score: Math.min(
          100,
          Math.round(completion * 0.8)
        ),
        matched: [],
        missing: [],
      };
    }

    const words = jdText.match(
      /\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b/g
    ) || [];

    const stopWords = new Set([
      "the",
      "and",
      "for",
      "with",
      "that",
      "this",
      "from",
      "you",
      "your",
      "are",
      "our",
      "will",
      "have",
      "has",
      "into",
      "their",
      "they",
      "about",
      "work",
      "working",
      "using",
      "role",
      "job",
      "candidate",
      "should",
      "must",
      "ability",
      "strong",
      "good",
      "team",
      "years",
    ]);

    const keywords = [
      ...new Set(
        words.filter(
          (word) =>
            !stopWords.has(word) &&
            word.length >= 3
        )
      ),
    ];

    const matched = keywords.filter((keyword) =>
      resumeText.includes(keyword)
    );

    const missing = keywords
      .filter(
        (keyword) =>
          !resumeText.includes(keyword)
      )
      .slice(0, 12);

    const keywordScore =
      keywords.length > 0
        ? Math.round(
            (matched.length / keywords.length) * 100
          )
        : 0;

    const score = Math.min(
      100,
      Math.round(
        keywordScore * 0.65 +
        completion * 0.35
      )
    );

    return {
      score,
      matched: matched.slice(0, 15),
      missing,
    };
  }, [resumeData, completion]);

  /* =====================================================
     GENERATE
  ===================================================== */

  const handleGenerateResume = () => {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: "smooth",
    });

    alert(
      `Resume analyzed successfully!\n\nATS Score: ${atsAnalysis.score}/100`
    );
  };

  return (
    <div className="app-shell">

      {/* =================================================
          TOPBAR
      ================================================= */}

      <header className="topbar">

        <div className="brand">

          <div className="brand-mark">
            ✦
          </div>

          <div>
            <div className="brand-name">
              Resume<span>AI</span>
            </div>

            <div className="brand-subtitle">
              Intelligent Resume Studio
            </div>
          </div>

        </div>

        <nav className="top-navigation">

          <button className="nav-item active">
            Builder
          </button>

          <button className="nav-item">
            Templates
          </button>

          <button className="nav-item">
            ATS Analyzer
          </button>

        </nav>

        <div className="top-actions">

          <div className="status-pill">
            <span className="status-dot"></span>
            Autosaved
          </div>

          <div className="avatar">
            R
          </div>

        </div>

      </header>


      {/* =================================================
          HERO
      ================================================= */}

      <section className="dashboard-intro">

        <div>

          <div className="eyebrow">
            <span>✦</span>
            AI-POWERED RESUME BUILDER
          </div>

          <h1>
            Build a resume that
            <span> gets noticed.</span>
          </h1>

          <p>
            Create a polished, ATS-friendly resume
            tailored to your target role.
          </p>

        </div>

        <div className="completion-card">

          <div className="completion-top">

            <div>
              <span className="completion-label">
                RESUME COMPLETION
              </span>

              <strong>
                {completion}%
              </strong>
            </div>

            <div className="completion-ring">
              {completion}%
            </div>

          </div>

          <div className="completion-track">
            <div
              className="completion-fill"
              style={{
                width: `${completion}%`,
              }}
            ></div>
          </div>

          <span className="completion-message">
            {completion >= 80
              ? "Your resume is looking strong."
              : "Keep adding information to strengthen your resume."}
          </span>

        </div>

      </section>


      {/* =================================================
          WORKSPACE
      ================================================= */}

      <main className="workspace">

        <section className="builder-area">

          <div className="workspace-heading">

            <div>
              <span className="workspace-kicker">
                RESUME BUILDER
              </span>

              <h2>
                Tell us about yourself
              </h2>

              <p>
                Complete each section and watch your
                resume update automatically.
              </p>
            </div>

            <div className="section-count">
              8 sections
            </div>

          </div>


          {/* =================================================
              PERSONAL
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="01"
              title="Personal Information"
              description="How recruiters can reach you"
            />

            <div className="input-grid">

              <InputField
                label="Full Name"
                name="name"
                value={resumeData.name}
                placeholder="Your full name"
                onChange={handleInputChange}
              />

              <InputField
                label="Email Address"
                name="email"
                type="email"
                value={resumeData.email}
                placeholder="you@example.com"
                onChange={handleInputChange}
              />

              <InputField
                label="Phone Number"
                name="phone"
                value={resumeData.phone}
                placeholder="+91 XXXXX XXXXX"
                onChange={handleInputChange}
              />

              <InputField
                label="Location"
                name="location"
                value={resumeData.location}
                placeholder="Bhubaneswar, Odisha"
                onChange={handleInputChange}
              />

              <InputField
                label="LinkedIn"
                name="linkedin"
                value={resumeData.linkedin}
                placeholder="linkedin.com/in/username"
                onChange={handleInputChange}
              />

              <InputField
                label="GitHub"
                name="github"
                value={resumeData.github}
                placeholder="github.com/username"
                onChange={handleInputChange}
              />
              </div>

</section>
                        {/* =================================================
              FONT CUSTOMIZATION
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="02"
              title="Font Customization"
              description="Choose the font style for your entire resume"
            />

            <div className="font-customization">

              {/* FONT FAMILY */}

              <div className="font-control">

                <label>Font Family</label>

                <select
                  value={resumeData.fontFamily}
                  onChange={(e) =>
                    setResumeData((prev) => ({
                      ...prev,
                      fontFamily: e.target.value,
                    }))
                  }
                >

                  <option value="font-calibri">
                    Calibri
                  </option>

                  <option value="font-times-new-roman">
                    Times New Roman
                  </option>

                  <option value="font-helvetica">
                    Helvetica
                  </option>

                </select>

              </div>


              {/* FONT WEIGHT */}

              <div className="font-control">

                <label>Font Weight</label>

                <select
                  value={resumeData.fontWeight}
                  onChange={(e) =>
                    setResumeData((prev) => ({
                      ...prev,
                      fontWeight: e.target.value,
                    }))
                  }
                >

                  <option value="normal">
                    Regular
                  </option>

                  <option value="bold">
                    Bold
                  </option>

                </select>

              </div>

            </div>

          </section>

          {/* =================================================
              PROFILE
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="02"
              title="Professional Profile"
              description="Position yourself for the role you want"
            />

            <InputField
              label="Target Role"
              name="role"
              value={resumeData.role}
              placeholder="e.g. Data Analyst"
              onChange={handleInputChange}
            />

            <TextAreaField
              label="Professional Summary"
              name="summary"
              value={resumeData.summary}
              placeholder="Write 3-4 lines describing your strongest skills, experience and value..."
              rows="5"
              onChange={handleInputChange}
            />

          </section>


          {/* =================================================
              EDUCATION
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="03"
              title="Education"
              description="Your academic background"
            />

            <div className="input-grid">

              <InputField
                label="Degree"
                name="degree"
                value={resumeData.degree}
                placeholder="B.Tech in Electronics & Communication"
                onChange={handleInputChange}
              />

              <InputField
                label="College / University"
                name="college"
                value={resumeData.college}
                placeholder="University name"
                onChange={handleInputChange}
              />

              <InputField
                label="CGPA / Percentage"
                name="cgpa"
                value={resumeData.cgpa}
                placeholder="8.5 / 85%"
                onChange={handleInputChange}
              />

              <InputField
                label="Graduation Year"
                name="year"
                value={resumeData.year}
                placeholder="2026"
                onChange={handleInputChange}
              />

            </div>

          </section>


          {/* =================================================
              SKILLS
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="04"
              title="Technical Skills"
              description="Organize your skills into recruiter-friendly categories"
            />

            <div className="input-grid">

              <TextAreaField
                label="Programming Languages"
                name="programming"
                value={resumeData.programming}
                placeholder="Python, Java, C, JavaScript..."
                rows="3"
                onChange={handleInputChange}
              />

              <TextAreaField
                label="Core Skills"
                name="coreSkills"
                value={resumeData.coreSkills}
                placeholder="Data Analysis, OOP, DSA, Problem Solving..."
                rows="3"
                onChange={handleInputChange}
              />

              <TextAreaField
                label="Tools & Technologies"
                name="tools"
                value={resumeData.tools}
                placeholder="Excel, Power BI, Git, Jupyter Notebook..."
                rows="3"
                onChange={handleInputChange}
              />

              <TextAreaField
                label="Databases"
                name="databases"
                value={resumeData.databases}
                placeholder="MySQL, PostgreSQL, SQL..."
                rows="3"
                onChange={handleInputChange}
              />

              <TextAreaField
                label="Soft Skills"
                name="softSkills"
                value={resumeData.softSkills}
                placeholder="Communication, Teamwork, Leadership..."
                rows="3"
                onChange={handleInputChange}
              />

            </div>

          </section>


          {/* =================================================
              PROJECTS
          ================================================= */}


<section className="builder-card">

  <CardHeading
    number="05"
    title="Projects"
    description="Show recruiters what you can actually build"
  />

  {resumeData.projects.map((project, index) => (

    <div
      className="repeatable-block"
      key={index}
    >

      <InputField
        label="Project Title"
        value={project.title}
        placeholder="e.g. Regional Language Identification"
        onChange={(e) =>
          handleProjectChange(
            index,
            "title",
            e.target.value
          )
        }
      />

      <InputField
        label="Technologies Used"
        value={project.technologies}
        placeholder="Python, CNN, TensorFlow, SQL..."
        onChange={(e) =>
          handleProjectChange(
            index,
            "technologies",
            e.target.value
          )
        }
      />

      <TextAreaField
        label="Project Description"
        value={project.description}
        placeholder="Describe the problem, your contribution, technologies used and measurable result..."
        rows="5"
        onChange={(e) =>
          handleProjectChange(
            index,
            "description",
            e.target.value
          )
        }
      />

    </div>

  ))}

  <button
    type="button"
    className="add-button"
    onClick={addProject}
  >
    + Add Another Project
  </button>

</section>
         


          {/* =================================================
              EXPERIENCE
          ================================================= */}

<section className="builder-card">

  <CardHeading
    number="06"
    title="Internships & Experience"
    description="Add internships, work experience and relevant roles"
  />

  {resumeData.experiences.map((experience, index) => (

    <div
      className="repeatable-block"
      key={index}
    >

      <div className="input-grid">

        <InputField
          label="Company / Organization"
          value={experience.company}
          placeholder="IBM SkillsBuild"
          onChange={(e) =>
            handleExperienceChange(
              index,
              "company",
              e.target.value
            )
          }
        />

        <InputField
          label="Role"
          value={experience.role}
          placeholder="Data Analyst Intern"
          onChange={(e) =>
            handleExperienceChange(
              index,
              "role",
              e.target.value
            )
          }
        />

        <InputField
          label="Duration"
          value={experience.duration}
          placeholder="Jun 2024 – Aug 2024"
          onChange={(e) =>
            handleExperienceChange(
              index,
              "duration",
              e.target.value
            )
          }
        />

      </div>

      <TextAreaField
        label="Responsibilities & Achievements"
        value={experience.description}
        placeholder="Describe responsibilities, tools used, achievements and measurable outcomes..."
        rows="5"
        onChange={(e) =>
          handleExperienceChange(
            index,
            "description",
            e.target.value
          )
        }
      />

    </div>

  ))}

  <button
    type="button"
    className="add-button"
    onClick={addExperience}
  >
    + Add Another Experience
  </button>

</section>

          {/* =================================================
              CERTIFICATIONS
          ================================================= */}

          <section className="builder-card">

            <CardHeading
              number="07"
              title="Certifications"
              description="Add certifications that strengthen your profile"
            />

            <TextAreaField
              label="Certifications"
              name="certifications"
              value={resumeData.certifications}
              placeholder="Microsoft Data Analytics — Microsoft
IBM SkillsBuild Data Analytics — CSRBOX
Google Data Analytics — Coursera"
              rows="5"
              onChange={handleInputChange}
            />

          </section>


          {/* =================================================
              ATS
          ================================================= */}

          <section className="builder-card ai-card">

            <div className="ai-glow"></div>

            <CardHeading
              number="08"
              title="AI / ATS Optimization"
              description="Compare your resume against a specific job"
              ai
            />

            <div className="ai-info">

              <div className="ai-info-icon">
                ✦
              </div>

              <div>

                <strong>
                  Improve your ATS match
                </strong>

                <p>
                  Paste the job description below.
                  ResumeAI will compare important
                  keywords against your resume.
                </p>

              </div>

            </div>

            <TextAreaField
              label="Job Description"
              name="jd"
              value={resumeData.jd}
              placeholder="Paste the job description here..."
              rows="9"
              onChange={handleInputChange}
            />

            {resumeData.jd && (
              <div className="keyword-analysis">

                <div className="analysis-title">
                  ATS KEYWORD ANALYSIS
                </div>

                <div className="analysis-score">
                  <strong>
                    {atsAnalysis.score}
                  </strong>
                  <span>/100</span>
                </div>

                <div className="keyword-columns">

                  <div>
                    <h4>
                      ✓ Matching Keywords
                    </h4>

                    <div className="keyword-list">
                      {atsAnalysis.matched.length > 0
                        ? atsAnalysis.matched.map(
                            (keyword) => (
                              <span
                                key={keyword}
                              >
                                {keyword}
                              </span>
                            )
                          )
                        : (
                          <small>
                            No matches yet.
                          </small>
                        )}
                    </div>

                  </div>

                  <div>
                    <h4>
                      ! Consider Adding
                    </h4>

                    <div className="keyword-list missing">
                      {atsAnalysis.missing.length > 0
                        ? atsAnalysis.missing.map(
                            (keyword) => (
                              <span
                                key={keyword}
                              >
                                {keyword}
                              </span>
                            )
                          )
                        : (
                          <small>
                            Excellent keyword match.
                          </small>
                        )}
                    </div>

                  </div>

                </div>

              </div>
            )}

          </section>


          <button
            className="generate-button"
            onClick={handleGenerateResume}
          >

            <span className="generate-icon">
              ✦
            </span>

            <span>
              Analyze & Generate Resume
            </span>

            <span className="arrow">
              →
            </span>

          </button>

          <p className="privacy-note">
            🔒 Your information stays in your browser while building your resume.
          </p>

        </section>


        {/* =================================================
            LIVE PREVIEW
        ================================================= */}

        <aside className="preview-area">

          <div className="preview-toolbar">

            <div>

              <span>
                LIVE PREVIEW
              </span>

              <h2>
                Your Resume
              </h2>

            </div>

          </div>


          <div className="paper-container">

            <div className={`resume-paper ${resumeData.fontFamily}`}>

              {/* HEADER */}

              <div className="resume-top">

                <h1>
                  {resumeData.name ||
                    "YOUR NAME"}
                </h1>

                <h2>
                  {resumeData.role ||
                    "Professional Title"}
                </h2>

                <div className="resume-contact">

                  {resumeData.email && (
                    <span>
                      {resumeData.email}
                    </span>
                  )}

                  {resumeData.phone && (
                    <span>
                      {resumeData.phone}
                    </span>
                  )}

                  {resumeData.location && (
                    <span>
                      {resumeData.location}
                    </span>
                  )}

                </div>

                {(resumeData.linkedin ||
                  resumeData.github) && (

                  <div className="resume-links">

                    {resumeData.linkedin && (
                      <span>
                        {resumeData.linkedin}
                      </span>
                    )}

                    {resumeData.github && (
                      <span>
                        {resumeData.github}
                      </span>
                    )}

                  </div>

                )}

              </div>


              {/* PROFILE */}

              {resumeData.summary && (
                <ResumeSection title="PROFESSIONAL SUMMARY">

                  <p>
                    {resumeData.summary}
                  </p>

                </ResumeSection>
              )}


              {/* EDUCATION */}

              {(resumeData.degree ||
                resumeData.college) && (

                <ResumeSection title="EDUCATION">

                  <div className="resume-entry">

                    <strong>
                      {resumeData.degree}
                    </strong>

                    <div className="resume-entry-row">

                      <span>
                        {resumeData.college}
                      </span>

                      <span>
                        {resumeData.year}
                      </span>

                    </div>

                    {resumeData.cgpa && (
                      <small>
                        CGPA / Percentage:{" "}
                        {resumeData.cgpa}
                      </small>
                    )}

                  </div>

                </ResumeSection>
              )}


              {/* SKILLS */}

              {(resumeData.programming ||
                resumeData.coreSkills ||
                resumeData.tools ||
                resumeData.databases ||
                resumeData.softSkills) && (

                <ResumeSection title="TECHNICAL SKILLS">

                  {resumeData.programming && (
                    <SkillRow
                      title="Programming Languages"
                      value={
                        resumeData.programming
                      }
                    />
                  )}

                  {resumeData.coreSkills && (
                    <SkillRow
                      title="Core Skills"
                      value={
                        resumeData.coreSkills
                      }
                    />
                  )}

                  {resumeData.tools && (
                    <SkillRow
                      title="Tools & Technologies"
                      value={
                        resumeData.tools
                      }
                    />
                  )}

                  {resumeData.databases && (
                    <SkillRow
                      title="Databases"
                      value={
                        resumeData.databases
                      }
                    />
                  )}

                  {resumeData.softSkills && (
                    <SkillRow
                      title="Soft Skills"
                      value={
                        resumeData.softSkills
                      }
                    />
                  )}

                </ResumeSection>
              )}


              {/* EXPERIENCE */}

              {resumeData.experiences.some(
                (e) =>
                  e.company ||
                  e.description
              ) && (

                <ResumeSection title="EXPERIENCE">

                  {resumeData.experiences.map(
                    (experience, index) =>
                      (experience.company ||
                        experience.description) && (

                        <div
                          className="resume-entry"
                          key={index}
                        >

                          <strong>
                            {experience.role
                              ? `${experience.role} — ${experience.company}`
                              : experience.company}
                          </strong>

                          <div className="resume-entry-row">

                            <span>
                              {experience.company}
                            </span>

                            <span>
                              {experience.duration}
                            </span>

                          </div>

                          <p>
                            {experience.description}
                          </p>

                        </div>

                      )
                  )}

                </ResumeSection>
              )}


              {/* PROJECTS */}

              {resumeData.projects.some(
                (p) =>
                  p.title ||
                  p.description
              ) && (

                <ResumeSection title="PROJECTS">

                  {resumeData.projects.map(
                    (project, index) =>
                      (project.title ||
                        project.description) && (

                        <div
                          className="resume-entry"
                          key={index}
                        >

                          <strong>
                            {project.title}
                          </strong>

                          {project.technologies && (
                            <small>
                              Technologies:{" "}
                              {project.technologies}
                            </small>
                          )}

                          <p>
                            {project.description}
                          </p>

                        </div>

                      )
                  )}

                </ResumeSection>
              )}


              {/* CERTIFICATIONS */}

              {resumeData.certifications && (

                <ResumeSection title="CERTIFICATIONS">

                  <p>
                    {resumeData.certifications}
                  </p>

                </ResumeSection>
              )}


              {!resumeData.name &&
                !resumeData.summary &&
                !resumeData.degree &&
                !resumeData.programming &&
                !resumeData.projects.some(
                  (p) =>
                    p.title ||
                    p.description
                ) && (

                <div className="preview-empty">

                  <div className="preview-empty-icon">
                    ✦
                  </div>

                  <h3>
                    Your resume starts here
                  </h3>

                  <p>
                    Start filling in your details
                    and watch your resume come
                    together.
                  </p>

                </div>
              )}

            </div>

          </div>


          {/* =================================================
              ATS SCORE CARD
          ================================================= */}

          <div className="ats-score-card">

            <div className="ats-score-icon">
              ✦
            </div>

            <div className="ats-score-content">

              <span>
                ATS SCORE
              </span>

              <strong>
                {atsAnalysis.score >= 80
                  ? "Strong Match"
                  : atsAnalysis.score >= 60
                  ? "Good Foundation"
                  : "Needs Improvement"}
              </strong>

              <p>
                {resumeData.jd
                  ? "Based on resume completion and JD keyword matching."
                  : "Paste a job description to calculate a targeted ATS score."}
              </p>

            </div>

            <div className="ats-score-number">
              {atsAnalysis.score}
            </div>

          </div>

        </aside>

      </main>

    </div>
  );
};


/* =========================================================
   CARD HEADING
========================================================= */

const CardHeading = ({
  number,
  title,
  description,
  ai = false,
}) => {
  return (
    <div className="card-heading">

      <div
        className={
          ai
            ? "ai-section-icon"
            : "section-icon"
        }
      >
        {ai ? "✦" : number}
      </div>

      <div>

        <h3>
          {title}
        </h3>

        <p>
          {description}
        </p>

      </div>

      {ai && (
        <span className="ai-badge">
          AI
        </span>
      )}

    </div>
  );
};


/* =========================================================
   INPUT FIELD
========================================================= */

const InputField = ({
  label,
  name,
  value,
  placeholder,
  onChange,
  type = "text",
}) => {
  return (
    <div className="field-wrapper">

      <label>
        {label}
      </label>

      <input
        type={type}
        name={name}
        value={value || ""}
        onChange={onChange}
        placeholder={placeholder}
      />

    </div>
  );
};


/* =========================================================
   TEXTAREA
========================================================= */

const TextAreaField = ({
  label,
  name,
  value,
  placeholder,
  rows = 4,
  onChange,
}) => {
  return (
    <div className="field-wrapper">

      <label>
        {label}
      </label>

      <textarea
        name={name}
        value={value || ""}
        onChange={onChange}
        placeholder={placeholder}
        rows={rows}
      />

    </div>
  );
};


/* =========================================================
   SKILL ROW
========================================================= */

const SkillRow = ({
  title,
  value,
}) => {
  return (
    <div className="skill-row">

      <strong>
        {title}:
      </strong>

      <span>
        {value}
      </span>

    </div>
  );
};


/* =========================================================
   RESUME SECTION
========================================================= */

const ResumeSection = ({
  title,
  children,
}) => {
  return (
    <section className="resume-section">

      <h3>
        {title}
      </h3>

      {children}

    </section>
  );
};


export default App;

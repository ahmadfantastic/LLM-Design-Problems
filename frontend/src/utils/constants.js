export const evaluationCriteria = [
    {
      key: 'scenario',
      name: 'Scenario Quality',
      description: 'How realistic, clear, and helpful is the scenario provided for the design problem?',
      score_2: 'The scenario is credible, mirrors authentic practice in the discipline, and explicitly supports learners in applying project knowledge to a realistic decision or trade-off.',
      score_1: 'The scenario is somewhat plausible but has minor gaps, simplifications, or contextual mismatches that could limit the transfer of learning.',
      score_0: 'The scenario is implausible, factually wrong, or so generic that it does not foster meaningful application.',
      weight: 2
    },
    {
      key: 'alignment',
      name: 'Alignment',
      description: 'How well does the design problem align with the targeted learning objectives?',
      score_2: 'The problem directly measures the target learning outcome(s)',
      score_1: 'The problem touches the target learning outcome(s) but also drifts into unrelated skills or omits part of the intended outcome.',
      score_0: 'There is little or no correspondence between the problem and the target target learning outcome(s).',
      weight: 3
    },
    {
      key: 'complexity',
      name: 'Cognitive Complexity',
      description: 'Does the design problem test higher-order thinking skills (Bloom\'s Taxonomy)?',
      score_2: 'Predominant demand is Analyze, Evaluate, Create (higher-order thinking). Students must justify their reasoning, compare alternatives, or design a novel solution.',
      score_1: 'Contains explicit hints or significant demands involving remembering or understanding (lower-order thinking).',
      score_0: 'Primarily lower-order (remember, list, define) with no substantive analysis or synthesis required.',
      weight: 3
    },
    {
      key: 'clarity',
      name: 'Clarity & Specificity',
      description: 'Is the design problem wording clear, unambiguous, and precise?',
      score_2: 'Unambiguous, concise, and self-contained; key terms are defined; and deliverables are explicit.',
      score_1: 'Mostly clear but contains minor ambiguities (e.g., vague constraints, undefined terms) that could cause uneven interpretations.',
      score_0: 'Vague, confusing, or contradictory instructions; missing critical details.',
      weight: 1
    },
    {
      key: 'feasibility',
      name: 'Feasibility',
      description: 'Can a well-prepared student answer within 30 minutes given the scope?',
      score_2: 'Workload fits the stated 30-minute limit and can be answered in a short paragraph or schematic; students have the required knowledge.',
      score_1: 'Slightly over/under the intended scope; may pressure time or require modest outside knowledge.',
      score_0: 'Unrealistic for allotted time or demands resources not provided (e.g., lengthy calculations, external research).',
      weight: 1
    }
  ]
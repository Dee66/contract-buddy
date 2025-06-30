// 🟪 ARCH: Clean, business-aligned sidebar for CodeCraft AI documentation

module.exports = {
  docs: [
    'index',
    'benchmarking',
    'checklist',
    'cost_tracking',
    'dependency_management',
    {
      type: 'category',
      label: 'Foundation',
      items: [
        'foundation/architecture_blueprint',
        'foundation/business_problem_value',
        'foundation/foundation_readme',
        'foundation/key_activities',
        'foundation/model_strategy',
        'foundation/objective',
        'foundation/risk_constraints',
      ],
    },
    {
      type: 'category',
      label: 'Core',
      items: [
        'core/benchmarking_optimization',
        'core/core_readme',
        'core/data_pipeline_processing',
        'core/data_sourcing',
        'core/dev_environment_data',
        'core/evaluation_plan',
        'core/key_activities',
        'core/model_implementation_experimentation',
        'core/objective',
        'core/stakeholder_review',
      ],
    },
    {
      type: 'category',
      label: 'Build',
      items: [
        'build/api_integration',
        'build/build_readme',
        'build/deployment_infrastructure',
        'build/key_activities',
        'build/objective',
        'build/observability_monitoring',
        'build/operational_playbook',
        'build/testing_validation',
        'build/user_interface',
      ],
    },
    {
      type: 'category',
      label: 'Configuration',
      items: [
        'configuration/config_management_enhancements',
        'configuration/config_schema',
        'configuration/configuration_readme',
      ],
    },
    {
      type: 'category',
      label: 'Portfolio',
      items: [
        'portfolio/future_roadmap',
        'portfolio/key_activities',
        'portfolio/objective',
        'portfolio/portfolio_readme',
        'portfolio/ultimate_readme',
        'portfolio/unique_value',
        'portfolio/verbal_narrative',
      ],
    },
    {
      type: 'category',
      label: 'DevOps',
      items: [
        'devops/strategy',
      ],
    },
    {
      type: 'category',
      label: 'Security',
      items: [
        'security/security',
      ],
    },
  ],
};

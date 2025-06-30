import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'dc2'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'fb1'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '203'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '56e'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/benchmarking',
                component: ComponentCreator('/docs/benchmarking', 'cd5'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/api_integration',
                component: ComponentCreator('/docs/build/api_integration', '2fe'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/build_readme',
                component: ComponentCreator('/docs/build/build_readme', '3ed'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/deployment_infrastructure',
                component: ComponentCreator('/docs/build/deployment_infrastructure', '79c'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/key_activities',
                component: ComponentCreator('/docs/build/key_activities', '8f7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/objective',
                component: ComponentCreator('/docs/build/objective', 'bbf'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/observability_monitoring',
                component: ComponentCreator('/docs/build/observability_monitoring', '0ce'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/operational_playbook',
                component: ComponentCreator('/docs/build/operational_playbook', '38b'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/testing_validation',
                component: ComponentCreator('/docs/build/testing_validation', 'b31'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/build/user_interface',
                component: ComponentCreator('/docs/build/user_interface', '1eb'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/checklist',
                component: ComponentCreator('/docs/checklist', '433'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/configuration/config_management_enhancements',
                component: ComponentCreator('/docs/configuration/config_management_enhancements', 'a71'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/configuration/config_schema',
                component: ComponentCreator('/docs/configuration/config_schema', 'd40'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/configuration/configuration_readme',
                component: ComponentCreator('/docs/configuration/configuration_readme', 'c22'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/benchmarking_optimization',
                component: ComponentCreator('/docs/core/benchmarking_optimization', 'c96'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/core_readme',
                component: ComponentCreator('/docs/core/core_readme', '364'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/data_pipeline_processing',
                component: ComponentCreator('/docs/core/data_pipeline_processing', '14b'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/data_sourcing',
                component: ComponentCreator('/docs/core/data_sourcing', 'ab7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/dev_environment_data',
                component: ComponentCreator('/docs/core/dev_environment_data', 'f17'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/evaluation_plan',
                component: ComponentCreator('/docs/core/evaluation_plan', '8e9'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/key_activities',
                component: ComponentCreator('/docs/core/key_activities', '517'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/model_implementation_experimentation',
                component: ComponentCreator('/docs/core/model_implementation_experimentation', '7f2'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/objective',
                component: ComponentCreator('/docs/core/objective', '700'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/core/stakeholder_review',
                component: ComponentCreator('/docs/core/stakeholder_review', '430'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/cost_tracking',
                component: ComponentCreator('/docs/cost_tracking', '647'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/dependency_management',
                component: ComponentCreator('/docs/dependency_management', '512'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/devops/strategy',
                component: ComponentCreator('/docs/devops/strategy', '7d4'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/architecture_blueprint',
                component: ComponentCreator('/docs/foundation/architecture_blueprint', '5cb'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/business_problem_value',
                component: ComponentCreator('/docs/foundation/business_problem_value', '719'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/foundation_readme',
                component: ComponentCreator('/docs/foundation/foundation_readme', 'ff3'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/key_activities',
                component: ComponentCreator('/docs/foundation/key_activities', '79b'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/model_strategy',
                component: ComponentCreator('/docs/foundation/model_strategy', '0cc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/objective',
                component: ComponentCreator('/docs/foundation/objective', '9ce'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/foundation/risk_constraints',
                component: ComponentCreator('/docs/foundation/risk_constraints', 'ccc'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/future_roadmap',
                component: ComponentCreator('/docs/portfolio/future_roadmap', '5c7'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/key_activities',
                component: ComponentCreator('/docs/portfolio/key_activities', 'bec'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/objective',
                component: ComponentCreator('/docs/portfolio/objective', '9a9'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/portfolio_readme',
                component: ComponentCreator('/docs/portfolio/portfolio_readme', '420'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/ultimate_readme',
                component: ComponentCreator('/docs/portfolio/ultimate_readme', 'e64'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/unique_value',
                component: ComponentCreator('/docs/portfolio/unique_value', '859'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/portfolio/verbal_narrative',
                component: ComponentCreator('/docs/portfolio/verbal_narrative', '7c4'),
                exact: true,
                sidebar: "docs"
              },
              {
                path: '/docs/security/',
                component: ComponentCreator('/docs/security/', 'ee2'),
                exact: true,
                sidebar: "docs"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];

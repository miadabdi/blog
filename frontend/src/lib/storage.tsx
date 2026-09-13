import type { Post, Project } from '@/lib/types';

export const posts: Post[] = [
  {
    id: 'building-microservices-nodejs-docker',
    title: 'Building Microservices with Node.js and Docker',
    description:
      'A comprehensive guide to architecting scalable microservices using containerization and orchestration.',
    date: '2024-01-15',
    readTime: '8 min read',
    tags: ['Node.js', 'Docker', 'Microservices'],
    featured: true,
    image: '/microservices-architecture-diagram-with-containers.jpg',
    content: `
      <p>This post walks through design considerations for microservices, how to containerize Node.js services with Docker, and deployment patterns for orchestration.</p>
      <p>Includes examples of service boundaries, health checks, and lightweight communication strategies.</p>
    `,
  },
  {
    id: 'optimizing-database-performance',
    title: 'Optimizing Database Performance in Production',
    description:
      'Strategies for query optimization, indexing, and connection pooling in high-traffic applications.',
    date: '2024-01-08',
    readTime: '12 min read',
    tags: ['PostgreSQL', 'Performance', 'Database'],
    image: '/database-performance-monitoring-dashboard.jpg',
    content: `
      <p>Covers indexing strategies, query profiling, and configuration tweaks to improve throughput and reduce latency.</p>
      <p>Also discusses monitoring and alerting for database health in production environments.</p>
    `,
  },
  {
    id: 'infrastructure-as-code-terraform',
    title: 'Infrastructure as Code with Terraform',
    description: 'Managing cloud infrastructure declaratively and implementing GitOps workflows.',
    date: '2024-01-01',
    readTime: '10 min read',
    tags: ['Terraform', 'AWS', 'DevOps'],
    image: '/terraform-infrastructure-code-on-screen.jpg',
    content: `
      <p>Introduces best practices for writing reusable Terraform modules, remote state management, and collaborating via GitOps.</p>
      <p>Examples include environment promotion and securing secrets in CI/CD pipelines.</p>
    `,
  },
  {
    id: 'implementing-event-driven-architecture',
    title: 'Implementing Event-Driven Architecture',
    description:
      'Designing resilient systems with message queues, event sourcing, and CQRS patterns.',
    date: '2023-12-20',
    readTime: '15 min read',
    tags: ['Architecture', 'Events', 'Patterns'],
    image: '/event-driven-architecture-flow-diagram.jpg',
    content: `
      <p>Discusses event-driven design patterns, trade-offs of eventual consistency, and practical examples using message brokers.</p>
      <p>Includes guidance on partitioning events, schema evolution, and replayability.</p>
    `,
  },
];

export const projects: Project[] = [
  {
    id: 'distributed-task-queue',
    title: 'Distributed Task Queue System',
    description: 'High-performance task processing system built with Redis, Node.js, and Docker.',
    tech: ['Node.js', 'Redis', 'Docker', 'Kubernetes'],
    github: '#',
    demo: '#',
    featured: true,
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'realtime-analytics-pipeline',
    title: 'Real-time Analytics Pipeline',
    description:
      'Stream processing pipeline for real-time data analytics using Apache Kafka, PostgreSQL, and custom dashboards.',
    tech: ['Python', 'Kafka', 'PostgreSQL', 'Grafana'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'api-gateway-microservices',
    title: 'API Gateway & Service Mesh',
    description:
      'Enterprise-grade API gateway with service discovery, load balancing, and circuit breaker patterns.',
    tech: ['Go', 'Kong', 'Consul', 'Prometheus'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'blockchain-supply-chain',
    title: 'Blockchain Supply Chain Tracker',
    description:
      'Decentralized supply chain management system with smart contracts and transparency tracking.',
    tech: ['Solidity', 'Ethereum', 'React', 'Web3.js'],
    github: '#',
    demo: '#',
    featured: true,
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'ml-recommendation-engine',
    title: 'ML-Powered Recommendation Engine',
    description:
      'Personalized recommendation system using collaborative filtering and deep learning models.',
    tech: ['Python', 'TensorFlow', 'FastAPI', 'MongoDB'],
    github: '#',
    demo: '#',
    featured: true,
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'iot-monitoring-platform',
    title: 'IoT Device Monitoring Platform',
    description:
      'Real-time monitoring and alerting platform for IoT devices with MQTT protocol and time-series data.',
    tech: ['Node.js', 'MQTT', 'InfluxDB', 'Vue.js'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'serverless-image-processor',
    title: 'Serverless Image Processing Service',
    description:
      'Auto-scaling image optimization and transformation service using serverless architecture.',
    tech: ['AWS Lambda', 'S3', 'CloudFront', 'Sharp'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'graphql-federated-api',
    title: 'Federated GraphQL API',
    description:
      'Unified GraphQL API layer aggregating multiple microservices with Apollo Federation.',
    tech: ['GraphQL', 'Apollo', 'TypeScript', 'Redis'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
  {
    id: 'cicd-automation-platform',
    title: 'CI/CD Automation Platform',
    description:
      'Custom continuous integration and deployment platform with pipeline orchestration and rollback capabilities.',
    tech: ['Jenkins', 'GitLab CI', 'Ansible', 'Terraform'],
    github: '#',
    demo: '#',
    content: '<p>Detailed project description...</p>',
    images: ['/database-performance-monitoring-dashboard.jpg'],
  },
];

export function getProject(id: string): Project | undefined {
  return projects.find((p) => p.id === id);
}

export function getPost(id: string): Post | undefined {
  return posts.find((p) => p.id === id);
}

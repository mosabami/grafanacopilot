import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

const faqs = [
  {
    question: 'Does Azure Managed Grafana use the open-source version of Grafana?',
    answer: 'Azure Managed Grafana is built on Grafana Enterprise, which includes all open-source Grafana features plus enterprise-specific capabilities like enhanced security, advanced data sources, and premium support.'
  },
  {
    question: 'How can I use Grafana Enterprise plugins?',
    answer: 'Grafana Enterprise plugins are included with Azure Managed Grafana. You can access premium data sources, advanced panel types, and enterprise authentication features directly through the service.'
  },
  {
    question: 'Can I install my own plugin?',
    answer: 'Custom plugin installation depends on your service tier and security requirements. Contact Azure support to discuss custom plugin requirements and approval processes for your organization.'
  },
  {
    question: 'How does pricing work for Azure Managed Grafana?',
    answer: 'Pricing is based on the number of active users and hosting infrastructure costs. You only pay for what you use, with no minimum commitments. Enterprise customers can access volume discounts.'
  },
  {
    question: 'What data sources are supported?',
    answer: 'Azure Managed Grafana supports 150+ data sources including Azure Monitor, Azure Data Explorer, Application Insights, and many third-party systems. Azure-native sources are optimized for performance.'
  }
];

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="py-20 bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Frequently asked questions
          </h2>
          <p className="text-xl text-gray-600">
            Get answers to common questions about Azure Managed Grafana
          </p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg overflow-hidden"
            >
              <button
                onClick={() => toggleFAQ(index)}
                className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
              >
                <span className="font-semibold text-gray-900 pr-4">
                  {faq.question}
                </span>
                {openIndex === index ? (
                  <ChevronUp className="w-5 h-5 text-gray-500 flex-shrink-0" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-gray-500 flex-shrink-0" />
                )}
              </button>
              {openIndex === index && (
                <div className="px-6 pb-4">
                  <p className="text-gray-600 leading-relaxed">
                    {faq.answer}
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <p className="text-gray-600 mb-6">
            Still have questions? Our team is here to help.
          </p>
          <button className="bg-blue-600 text-white px-8 py-3 rounded-sm hover:bg-blue-700 transition-colors">
            Contact support
          </button>
        </div>
      </div>
    </section>
  );
};

export default FAQ;
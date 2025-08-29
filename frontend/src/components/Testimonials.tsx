import { Star } from 'lucide-react';

const testimonials = [
	{
		quote: 'The integration with Azure Monitor and Microsoft Entra ID made deployment seamless. Our team can now focus on insights instead of infrastructure management.',
		author: 'Jennifer Martinez',
		role: 'Cloud Architect',
		company: 'Global Financial Services',
		avatar:
			'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
	},
	{
		quote: 'One-click dashboard creation from Azure Portal charts saved us weeks of development time. The built-in high availability gives us peace of mind.',
		author: 'David Kim',
		role: 'Senior DevOps Engineer',
		company: 'Healthcare Technology Inc',
		avatar:
			'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
	},
	{
		quote: 'The comprehensive security features and compliance capabilities make it perfect for our enterprise requirements. Grafana Enterprise support is excellent.',
		author: 'Rachel Thompson',
		role: 'Infrastructure Manager',
		company: 'Manufacturing Solutions Ltd',
		avatar:
			'https://images.pexels.com/photos/1181686/pexels-photo-1181686.jpeg?auto=compress&cs=tinysrgb&w=150&h=150&dpr=2',
	},
];

const Testimonials = () => {
	return (
		<section className="py-20 bg-gradient-to-r from-blue-50 to-indigo-50">
			<div className="w-full px-4 sm:px-6 lg:px-8">
				<div className="text-center mb-16">
					<h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
						Trusted by enterprises worldwide
					</h2>
					<p className="text-xl text-gray-600">
						Organizations rely on Azure Managed Grafana for mission-critical
						observability
					</p>
				</div>

				<div className="grid lg:grid-cols-3 gap-8">
					{testimonials.map((testimonial, index) => (
						<div
							key={index}
							className="bg-white rounded-lg p-8 shadow-sm hover:shadow-lg transition-all duration-300"
						>
							<div className="flex items-center mb-4">
								{[...Array(5)].map((_, i) => (
									<Star
										key={i}
										className="w-5 h-5 text-yellow-400 fill-current"
									/>
								))}
							</div>

							<blockquote className="text-gray-700 mb-6 italic leading-relaxed">
								"{testimonial.quote}"
							</blockquote>

							<div className="flex items-center">
								<img
									src={testimonial.avatar}
									alt={testimonial.author}
									className="w-12 h-12 rounded-full object-cover mr-4"
								/>
								<div>
									<div className="font-semibold text-gray-900">
										{testimonial.author}
									</div>
									<div className="text-sm text-gray-600">
										{testimonial.role}, {testimonial.company}
									</div>
								</div>
							</div>
						</div>
					))}
				</div>

				<div className="mt-16 text-center">
					<div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center opacity-60">
						<div className="text-2xl font-bold text-gray-400">Fortune 500</div>
						<div className="text-2xl font-bold text-gray-400">Healthcare</div>
						<div className="text-2xl font-bold text-gray-400">Financial</div>
						<div className="text-2xl font-bold text-gray-400">Manufacturing</div>
					</div>
				</div>
			</div>
		</section>
	);
};

export default Testimonials;
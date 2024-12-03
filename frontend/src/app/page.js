"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Activity, Shield } from 'lucide-react';

import GradientBackground from '@/components/gradient-background';

export default function Home() {
	const [scrolling, setScrolling] = useState(false);
	const router = useRouter();

	const handleClick = () => {
		// Prevent interactions and enable scrolling
		setScrolling(true);

		// Enable scrolling and scroll to the bottom
		const container = document.querySelector('#scroll-container');
		if (container) {
			container.style.overflow = 'auto'; // Enable scrolling
			container.scrollTo({
				top: container.scrollHeight,
				behavior: 'smooth', // Smooth scrolling
			});

			// Wait for scrolling to finish using a timeout
			const checkIfScrolled = setInterval(() => {
				if (
					Math.ceil(container.scrollTop + container.clientHeight) >=
					container.scrollHeight
				) {
					clearInterval(checkIfScrolled); // Stop checking
					
					// Add a 0.7-second delay before navigating
					setTimeout(() => {
						router.push('/report'); // Navigate to /report
					}, 700);
				}
			}, 50); // Check every 50ms
		}
	};

	return (
		<div
			id="scroll-container"
			className={`w-full h-screen relative overflow-hidden ${
				scrolling ? 'pointer-events-none' : ''
			}`}
		>
			<div className="absolute z-20 w-full h-full flex flex-1 flex-col items-center justify-between">
				
				{/* Header component */}
				<div className='h-14 w-full' />
				
				<div className='w-full h-full flex flex-1 flex-col items-center justify-center gap-5'>
					<div className="h-16 w-16 flex items-center justify-center bg-white/15 backdrop-blur-md rounded-full border border-white/15 text-[#6E3CEC]">
						<Shield size={36} />
					</div>
					<h1 className="text-5xl font-bold text-white">Discover how secure your website is</h1>
					<p className="text-2xl font-medium text-neutral-500">
						Test the vulnerabilities in matter of seconds,
						<br />
						avoid potential risks threats on your company.
					</p>

					<div className="flex flex-row items-center bg-white/10 p-2 rounded-full border border-white/15 mt-8">
						<input
							type="text"
							placeholder="Enter your URL"
							className="w-64 bg-transparent outline-none px-2"
						/>
						<button
							onClick={handleClick}
							className="h-10 w-10 flex items-center justify-center rounded-full text-black bg-white"
						>
							<Activity size={18} />
						</button>
					</div>
				</div>
				
				<div className='pb-12'>Made with ❤️ by</div>
			</div>
			<GradientBackground />
		</div>
	);
}

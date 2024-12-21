"use client";

import { Shield } from 'lucide-react';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';

import GradientBackground from '@/components/gradient-background';
import SearchInput from '@/components/search-input';
import Tooltip from "@/components/tooltip";


export default function Home() {
	const [scrolling, setScrolling] = useState(false);
	const router = useRouter();

	const contributors = [
		{
			name: "Diane Dinh",
			image: "/image.png",
			github: "https://github.com/johndoe",
		},
		{
			name: "Jane Smith",
			image: "/image.png",
			github: "https://github.com/janesmith",
		},
		{
			name: "Alex Brown",
			image: "/image.png",
			github: "https://github.com/alexbrown",
		},
		{
			name: "Jane Smith",
			image: "/image.png",
			github: "https://github.com/janesmith",
		},
		{
			name: "Alex Brown",
			image: "/image.png",
			github: "https://github.com/alexbrown",
		},
		{
			name: "Jane Smith",
			image: "/image.png",
			github: "https://github.com/janesmith",
		}
	];

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
			<div className="absolute z-20 w-full h-full flex flex-1 flex-col items-center justify-between p-4 text-balance">
				
				{/* Header component */}
				<div className='h-14 w-full' />
				
				<div className='w-full h-full flex flex-1 flex-col items-center justify-center gap-5'>
					<div className="h-16 w-16 flex items-center justify-center bg-white/15 backdrop-blur-md rounded-full border border-white/15 text-[#6E3CEC]">
						<Shield size={36} />
					</div>
					<h1 className="text-3xl md:text-5xl font-bold text-white text-center">Discover how secure your website is</h1>
					<p className="text-base md:text-2xl font-medium text-neutral-500 text-center">
						Test the vulnerabilities in matter of seconds,
						<br />
						avoid potential risks threats on your company.
					</p>

					<SearchInput onClick={handleClick} />
				</div>
				
				<div className='pb-12 flex flex-row items-center gap-2'>
					<p>Made with ❤️ by </p>
					<div className="flex items-center">
						{contributors.map((contributor, index) => (
							<Tooltip key={index} content={contributor.name}>
								<a
									href={contributor.github}
									target="_blank"
									rel="noopener noreferrer"
									className="relative inline-block"
									style={{
										zIndex: contributors.length - index,
										marginLeft: index === 0 ? 0 : -12,
									}}
								>
									<Image
										src={contributor.image}
										alt={contributor.name}
										width={128}
										height={128}
										className="h-8 w-8 rounded-full border border-white shadow-lg object-cover"
									/>
								</a>
							</Tooltip>
						))}
					</div>
				</div>
			</div>
			<GradientBackground />
		</div>
	);
}


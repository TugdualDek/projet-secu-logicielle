import { Activity, Shield } from 'lucide-react';

import GradientBackground from '@/components/gradient-background';

export default function Home() {
	return (
		<div className='w-full h-screen relative overflow-hidden'>
			<div className="absolute z-20 w-full h-full flex flex-1 flex-col items-center justify-center gap-5">
				<div className='h-16 w-16 flex items-center justify-center bg-white/15 backdrop-blur-md rounded-full text-[#6E3CEC]'>
					<Shield size={36}  />
				</div>
				<h1 className="text-5xl font-bold text-white">Discover how secure your website is</h1>
				<p className="text-2xl font-medium text-neutral-500">Test the vulnerabilities in matter of seconds,<br/>avoid potential risks threats on your company.</p>
				
				<div className="flex flex-row items-center bg-white/10 p-2 rounded-full mt-8">
					<input type="text" placeholder="Enter your URL" className="w-64 bg-transparent outline-none px-2" />
					<button className="h-10 w-10 flex items-center justify-center rounded-full text-black bg-white">
						<Activity size={18} />
					</button>
				</div>
			</div>
			<GradientBackground />
		</div>
	);
}
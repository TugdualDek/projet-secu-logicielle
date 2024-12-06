import { Activity } from 'lucide-react';

const SearchInput = ({ onClick }) => {
    return (
        <div className="sticky top-0 flex flex-row items-center bg-white/10 p-2 rounded-full border border-white/15 mt-8">
            <input
                type="text"
                placeholder="Enter your URL"
                className="w-72 bg-transparent outline-none px-2"
            />
            <button
                onClick={onClick}
                className="h-10 w-10 flex items-center justify-center rounded-full text-black bg-white"
            >
                <Activity size={18} />
            </button>
        </div>
    );
};

export default SearchInput;
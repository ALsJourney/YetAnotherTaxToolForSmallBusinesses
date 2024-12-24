import { formatDate } from '../lib/utils';
import FileDownloadButton from "@/app/components/DownloadFileBtn";

interface Entry {
    id: number;
    date: number;
    revenue: number;
    cost: number;
    file_id: number;
}

interface EntriesData {
    data: Entry[];
}

export default function EntryList({ entries }: { entries: EntriesData }) {
    return (
        <ul className="space-y-4">
            {entries.data.map((entry) => (
                <li key={entry.id} className="border p-4 rounded">
                    <div className="flex justify-between">
                        <span className="font-semibold">Date: {formatDate(entry.date)}</span>
                        <span className="text-green-600">Total Revenue: {entry.revenue.toFixed(2)}€</span>
                    </div>
                    <div className="flex justify-between mt-2">
                        <span className="text-red-600">Total Cost: {entry.cost.toFixed(2)}€</span>
                        <span className="font-semibold">Total Profit: {(entry.revenue - entry.cost).toFixed(2)}€</span>
                    </div>
                    {entry.file_id && (
                        <FileDownloadButton fileId={entry.file_id} />
                    )}
                </li>
            ))}
        </ul>
    );
}

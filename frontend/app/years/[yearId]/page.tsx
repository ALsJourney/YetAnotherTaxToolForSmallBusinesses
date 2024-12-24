'use client';

import React, { useEffect, useRef, useState } from 'react';
import { getEntries, getProfit } from '../../lib/api';
import EntryList from '../../components/EntryList';
import AddEntryForm from '../../components/AddEntryForm';

interface YearPageProps {
    params: Promise<{
        yearId: string;
    }>;
}

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

interface Profit {
    profit: number;
}

export default function YearPage({ params }: YearPageProps) {
    const { yearId } = React.use(params);

    // `entries` should be an array of `Entry`
    const [entries, setEntries] = useState<EntriesData>({ data: [] });
    const [profit, setProfit] = useState<number>(0);
    const [loading, setLoading] = useState(true);
    const totalProfitRef = useRef<number>(0);

    useEffect(() => {
        async function fetchData() {
            try {
                // Fetch entries and profit data
                const entriesData: EntriesData = await getEntries(Number(yearId));
                const profitData: Profit = await getProfit(Number(yearId));

                totalProfitRef.current = profitData.profit;

                setProfit(profitData.profit);
                setEntries(entriesData);

            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [yearId]);

    if (loading) {
        return <div>Loading...</div>;
    }

    const refreshEntries = async () => {
        try {
            const updatedEntries: EntriesData = await getEntries(Number(yearId));
            setEntries(updatedEntries);
        } catch (error) {
            console.error('Error refreshing entries:', error);
        }
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-4">Year {yearId}</h1>
            <div className="mb-4">
                <h2 className="text-2xl font-semibold">Total Profit: {profit.toFixed(2)}€</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                    <h2 className="text-2xl font-semibold mb-2">Entries</h2>
                    <EntryList entries={entries} />
                </div>
                <div>
                    <h2 className="text-2xl font-semibold mb-2">Add New Entry</h2>
                    <AddEntryForm yearId={Number(yearId)} onEntryAdded={refreshEntries} />
                </div>
            </div>
        </div>
    );
}

'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { getYears } from '../lib/api'

interface Year {
    id: number;
    year: number;
}

interface YearData {
    data: Year[];
}

export default function YearList() {
    const [years, setYears] = useState<YearData>({ data: [] })
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        async function fetchYears() {
            try {
                const fetchedYears = await getYears()
                console.log('Fetched years:', fetchedYears)
                setYears(fetchedYears)
            } catch (err) {
                console.error('Error fetching years:', err)
                setError('Failed to fetch years. Please try again later.')
            }
        }
        fetchYears()
    }, [])

    if (error) {
        return <div className="text-red-500">{error}</div>
    }

    if (years.data.length === 0) {
        return <div>No years available.</div>
    }

    return (
        <ul className="space-y-2">
            {years.data.map((year: Year)  => (
                <li key={year.id}>
                    <Link href={`/years/${year.id}`} className="text-blue-600 hover:underline">
                        {year.year}
                    </Link>
                </li>
            ))}
        </ul>
    )
}


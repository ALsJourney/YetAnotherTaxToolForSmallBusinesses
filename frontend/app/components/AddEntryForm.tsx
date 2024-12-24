'use client';

import { useState, useEffect } from 'react';
import {createEntry, uploadFile, getCategories } from '../lib/api';

interface AddEntryFormProps {
    yearId: number;
    onEntryAdded: () => void;
}

interface FormData {
    revenue: number;
    cost: number;
    date: number;
    file: File | null;
    cat_id: number;
}

export default function AddEntryForm({ yearId, onEntryAdded }: AddEntryFormProps) {
    const [formData, setFormData] = useState<FormData>({
        revenue: 0,
        cost: 0,
        date: 0,
        file: null,
        cat_id: 1,
    });
    const [categories, setCategories] = useState<{ id: number; name: string }[]>([]);

    // Fetch categories on mount
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const categoriesData = await getCategories();
                setCategories(categoriesData);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };
        fetchCategories();
    }, []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        let fileId: number | null = null;

        if (formData.file) {
            try {
                fileId = await uploadFile(formData.file);
                console.log('Uploaded file ID:', fileId);
            } catch (error) {
                console.error('Error uploading file:', error);
                return;
            }
        }

        const payload = {
            revenue: formData.revenue,
            cost: formData.cost,
            date: formData.date,
            year_id: yearId,
            cat_id: formData.cat_id,
            file_id: fileId || null,
        };

        try {
            await createEntry(payload);

            // Trigger the callback to refresh entries
            onEntryAdded();

            // Reset the form
            setFormData({ revenue: 0, cost: 0, date: 0, file: null, cat_id: 1 });
        } catch (error) {
            console.error('Error creating entry:', error);
        }
    };



    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;

        if (e.target instanceof HTMLInputElement && e.target.type === "file") {
            const files = e.target.files;
            setFormData(prev => ({
                ...prev,
                file: files ? files[0] : null,
            }));
        } else {
            setFormData(prev => ({
                ...prev,
                [name]: name === 'revenue' || name === 'cost' || name === 'cat_id'
                    ? Number(value)
                    : name === 'date'
                        ? new Date(value).getTime() / 1000
                        : value,
            }));
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div>
                <label htmlFor="revenue" className="block text-sm font-medium text-gray-700">
                    Revenue
                </label>
                <input
                    type="number"
                    id="revenue"
                    name="revenue"
                    value={formData.revenue}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                    step="0.01"
                />
            </div>
            <div>
                <label htmlFor="cost" className="block text-sm font-medium text-gray-700">
                    Cost
                </label>
                <input
                    type="number"
                    id="cost"
                    name="cost"
                    value={formData.cost}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                    step="0.01"
                />
            </div>
            <div>
                <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                    Date
                </label>
                <input
                    type="date"
                    id="date"
                    name="date"
                    value={formData.date ? new Date(formData.date * 1000).toISOString().split('T')[0] : ''}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                />

            </div>
            <div>
                <label htmlFor="cat_id" className="block text-sm font-medium text-gray-700">
                    Category
                </label>
                <select
                    id="cat_id"
                    name="cat_id"
                    value={formData.cat_id}
                    onChange={handleChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                >
                    <option value="" disabled>Select a category</option>
                    {categories.map(category => (
                        <option key={category.id} value={category.id}>
                            {category.name}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <label htmlFor="file" className="block text-sm font-medium text-gray-700">
                    Receipt (optional)
                </label>
                <input
                    type="file"
                    id="file"
                    name="file"
                    onChange={handleChange}
                    className="mt-1 block w-full"
                />
            </div>
            <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
            >
                Add Entry
            </button>
        </form>
    );
}

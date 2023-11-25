// EditBill.js
import React, { useEffect, useState } from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import { useParams, useNavigate } from 'react-router-dom';

function EditBill() {
    const { billId } = useParams();
    const navigate = useNavigate();
    const [initialValues, setInitialValues] = useState({ title: '', content: '' });

    useEffect(() => {
        fetch(`http://localhost:5555/bill/${billId}`)
            .then(response => response.json())
            .then(data => setInitialValues({ title: data.bill.title, content: data.bill.content }))
            .catch(error => console.error('Error fetching bill details:', error));
    }, [billId]);

    const handleSubmit = async (values, { setSubmitting }) => {
        try {
            const response = await fetch(`http://localhost:5555/bill/${billId}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(values)
            });

            if (response.ok) {
                console.log('Bill updated successfully');
                navigate(`/bills/${billId}`);
            } else {
                console.error('Failed to update bill');
            }
        } catch (error) {
            console.error('Error:', error);
        }

        setSubmitting(false);
    };

    return (
        <div>
            <h2>Edit Bill</h2>
            <Formik initialValues={initialValues} enableReinitialize onSubmit={handleSubmit}>
                {({ isSubmitting }) => (
                    <Form>
                        <div>
                            <label htmlFor="title">Title</label>
                            <Field type="text" name="title" required />
                            <ErrorMessage name="title" component="div" />
                        </div>
                        <div>
                            <label htmlFor="content">Content</label>
                            <Field as="textarea" name="content" required />
                            <ErrorMessage name="content" component="div" />
                        </div>
                        <button type="submit" disabled={isSubmitting}>
                            Update Bill
                        </button>
                    </Form>
                )}
            </Formik>
        </div>
    );
}

export default EditBill;

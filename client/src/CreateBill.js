import React, {useState} from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';

function CreateBill({setBills}) {
    
    const initialValues = {
        title: '',
        content: ''
    };

    const handleSubmit = async (values, { setSubmitting }) => {
        
        try {
            const response = await fetch('/bill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming token-based auth
                },
                body: JSON.stringify(values)
            });
            console.log(response)
            if (response.ok) {
                console.log('Bill created successfully');
                response.json().then(data => {
                    setBills(oldBills => [...oldBills, data])

                })
            } else {
                console.error('Failed to create bill');
                // Handle errors here
            }
        } catch (error) {
            console.error('Error:', error);
        }

        setSubmitting(false);
    };

    return (
        <div>
            <h2>Create a New Bill</h2>
            <Formik initialValues={initialValues} onSubmit={handleSubmit}>
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
                            Create Bill
                        </button>
                    </Form>
                )}
            </Formik>
        </div>
    );
}

export default CreateBill;

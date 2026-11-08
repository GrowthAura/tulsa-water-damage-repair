'use client';
import { useState } from 'react';
import { SITE } from '../lib-meta';

/*
 * Non-emergency contact form. No delivery inbox exists in the source doc,
 * so this form does NOT pretend to send anything: on submit it says so
 * plainly and points at the phone. Wire it to the owner's inbox (e.g.
 * FormSubmit) before claiming it receives messages.
 */
export default function ContactForm() {
  const [sent, setSent] = useState(false);
  return (
    <div className="form-card">
      <h3>Non-Emergency Contact Form</h3>
      <p>For non-urgent questions, scheduling or claim paperwork.</p>
      {sent ? (
        <div className="form-note" role="status">
          <p>
            <strong>This form is not connected to an inbox yet.</strong> Your message was not
            sent anywhere. For the fastest help, call{' '}
            <a href={SITE.phoneHref}>{SITE.phone}</a> — answered 24/7.
          </p>
        </div>
      ) : (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setSent(true);
          }}
        >
          <label htmlFor="cf-name">Your name</label>
          <input id="cf-name" name="name" type="text" autoComplete="name" required />
          <label htmlFor="cf-phone">Phone</label>
          <input id="cf-phone" name="phone" type="tel" autoComplete="tel" required />
          <label htmlFor="cf-email">Email (optional)</label>
          <input id="cf-email" name="email" type="email" autoComplete="email" />
          <label htmlFor="cf-message">How can we help?</label>
          <textarea id="cf-message" name="message" rows={5} required />
          <button className="btn btn-navy" type="submit" style={{ width: '100%' }}>
            Send Message
          </button>
          <div className="form-note">
            <p>
              <strong>Emergencies:</strong> do not use this form — water keeps spreading while
              you wait for a reply. Call <a href={SITE.phoneHref}>{SITE.phone}</a> now.
            </p>
          </div>
        </form>
      )}
    </div>
  );
}

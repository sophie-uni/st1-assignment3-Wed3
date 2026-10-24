'''Patient and Practitioner construction and required-field validation,
and Appointment construction,
initial status and guarded cancellation.
Preserve the four original reference-test intentions: blank patient ID rejected;
a new appointment starts SCHEDULED;
cancellation changes status;
repeated cancellation is rejected.
Implement your own tests using the current imports and ValueError contract.'''
Example of uploading a csv file using the batching API of mixpanel.

ip and time fields are treated specially by mixpanel and are set as `meta` fields.
user_id is set as the distinct_id.
all other fields are set as properties.

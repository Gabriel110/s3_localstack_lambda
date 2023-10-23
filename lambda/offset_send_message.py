from read_s3_file import ReadFileS3
from send_message_sns import send_message_batch_to_sns
from handler import invoke_lambda

def offset_invoke_lambda_send_batch_sns(bucket_name, object_key, correlation_id, offset, context, event):
	file = ReadFileS3(bucket_name, object_key, correlation_id, offset)

	row_batch_array = []
	for row in file.get_csv_reader():
		row_batch_array.append(row)
		if len(row_batch_array) >= 10:
			send_message_batch_to_sns(row_batch_array, correlation_id)
			row_batch_array.clear()

	send_message_batch_to_sns(row_batch_array, correlation_id)

	new_offset = offset + file.body_lines.offset
	if new_offset < file.s3_object.content_length:
		new_event = {
			**event,
			"offset": new_offset,
			"correlation_id": correlation_id
		}
		invoke_lambda(context.function_name, new_event)
	else:
		# file.move_file_to_processed_folder()
		return
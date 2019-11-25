### Develop With Deere - Data Subscription Service (DSS) Example
****
[DSS Overview](https://developerqa.deere.com/#!documentation&doc=.%2Fmyjohndeere%2FsubscriptionApiOverviewContent.htm&anchor=)

Event Types:
* Subscription Verification
  * Used by the DSS Subscription API to validate a target endpoint
    * The target URL needs to return a 204 response for the DSS subscription to be activated.
* Field Operation
  * Send notification when field operation events occur
    * can be filtered by field operation type (ex: harvest, planting)
 
 ***
 #### Overview of Example
 * Create a new Field Operation subscription to send notifications when events occur
   * When creating the subscription:
     * set the targetEndpoint uri to invoke AWS API Gateway to process the event with AWS lambda function
        * Note: DSS expects a 204 response back within 5 seconds to be consider a valid delivery. If these requirements are not met, DSS will continue to send the event until the conditions are met. If the conditions continue to not be met over time, the subscription will be paused
     * set token value to the predetermined unique value so that the AWS API Gateway will forward the DSS event to your specific AWS lambda
 * Modify AWS lambda to send to desired email and other personal changes
   * Code changes can be made right in the AWS lambda console!
 * Kick off a field operation event that will invoke DSS and deliver the event to the subscription target uri
   * Receive email with map image and some field operation values
